"""SQLite logging integration using Loguru sinks for MCP tools.

This module implements Dan Andrew's suggestion to use Loguru sinks for 
SQLite logging, providing structured logging for MCP tool execution.

Features:
- Loguru custom sink for SQLite database
- Thread-safe database connections
- MCP tool-specific log schema
- Automatic database initialization
- Log retention and rotation
- Query utilities for admin UI
"""

import sqlite3
import threading
from pathlib import Path
from typing import Optional, Dict, Any, List
from datetime import datetime, timedelta
import json
from loguru import logger
import platformdirs

from my_mcp_server.config import ServerConfig
from my_mcp_server.decorators.base_logger_sink import BaseLoggerSink


class SQLiteLoggerSink(BaseLoggerSink):
    """Loguru sink for SQLite database logging with MCP tool support."""
    
    def __init__(self, config: Optional[ServerConfig] = None):
        """Initialize SQLite logging sink.
        
        Args:
            config: Server configuration for database path and retention
        """
        super().__init__(config)
        self._db_path = self._get_database_path()
        self._local = threading.local()
        self._initialize_database()
    
    def _get_database_path(self) -> Path:
        """Get platform-specific database path."""
        # Use the same path as config for consistency
        data_dir = Path(platformdirs.user_data_dir("my_mcp_server"))
        data_dir.mkdir(parents=True, exist_ok=True)
        # Use unified_logs.db to match config.py
        return data_dir / "unified_logs.db"
    
    def get_log_location(self) -> str:
        """Get the location where logs are stored.
        
        Returns:
            String path to the SQLite database file
        """
        return str(self._db_path)
    
    def _get_connection(self) -> sqlite3.Connection:
        """Get thread-local database connection."""
        if not hasattr(self._local, 'connection'):
            self._local.connection = sqlite3.connect(
                str(self._db_path),
                check_same_thread=False
            )
            # Try WAL mode for better concurrency, but fall back if it fails (Windows file locking)
            try:
                self._local.connection.execute("PRAGMA journal_mode=WAL")
                self._local.connection.execute("PRAGMA synchronous=NORMAL")
            except sqlite3.OperationalError:
                # Fall back to DELETE mode if WAL fails (common on Windows with certain file systems)
                self._local.connection.execute("PRAGMA journal_mode=DELETE")
                self._local.connection.execute("PRAGMA synchronous=FULL")
        return self._local.connection
    
    def _initialize_database(self):
        """Initialize database schema."""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        # Enhanced schema for MCP tool logging
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tool_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                level TEXT NOT NULL,
                message TEXT NOT NULL,
                tool_name TEXT,
                duration_ms INTEGER,
                status TEXT CHECK(status IN ('success', 'error', 'running')),
                input_args TEXT,  -- JSON
                output_summary TEXT,
                error_message TEXT,
                module TEXT,
                function TEXT,
                line INTEGER,
                extra_data TEXT,  -- JSON for additional context
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Create indexes for performance
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_timestamp ON tool_logs(timestamp)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_tool_name ON tool_logs(tool_name)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_status ON tool_logs(status)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_level ON tool_logs(level)")
        
        conn.commit()
    
    def __call__(self, message):
        """Loguru sink function - called for each log record.
        
        Args:
            message: Loguru message object with record data
        """
        record = message.record
        extra = record.get("extra", {})
        
        # Extract MCP tool-specific data from extra fields
        tool_name = extra.get("tool_name")
        duration_ms = extra.get("duration_ms")
        status = extra.get("status")
        input_args = extra.get("input_args")
        output_summary = extra.get("output_summary")
        error_message = extra.get("error_message")
        
        # Convert complex data to JSON
        input_args_json = json.dumps(input_args) if input_args else None
        extra_data_json = json.dumps({k: v for k, v in extra.items() 
                                    if k not in ['tool_name', 'duration_ms', 'status', 
                                               'input_args', 'output_summary', 'error_message']})
        
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO tool_logs (
                    timestamp, level, message, tool_name, duration_ms, status,
                    input_args, output_summary, error_message, module, function, 
                    line, extra_data
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                record["time"].strftime("%Y-%m-%d %H:%M:%S.%f"),
                record["level"].name,
                str(record["message"]),
                tool_name,
                duration_ms,
                status,
                input_args_json,
                output_summary,
                error_message,
                record.get("module"),
                record.get("function"),
                record.get("line"),
                extra_data_json if extra_data_json != '{}' else None
            ))
            
            conn.commit()
            
        except Exception as e:
            # Fallback to stderr if database write fails
            print(f"SQLite logging error: {e}")
    
    def cleanup_old_logs(self):
        """Remove logs older than retention period."""
        if not self.config.log_retention_days:
            return
            
        cutoff_date = datetime.now() - timedelta(days=self.config.log_retention_days)
        
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "DELETE FROM tool_logs WHERE timestamp < ?",
                (cutoff_date.strftime("%Y-%m-%d %H:%M:%S"),)
            )
            deleted_count = cursor.rowcount
            conn.commit()
            
            # Vacuum to reclaim space
            if deleted_count > 0:
                cursor.execute("VACUUM")
                
        except Exception as e:
            logger.error(f"Log cleanup failed: {e}")
    
    def get_logs(self, 
                 tool_name: Optional[str] = None,
                 status: Optional[str] = None,
                 start_date: Optional[datetime] = None,
                 end_date: Optional[datetime] = None,
                 limit: int = 1000) -> List[Dict[str, Any]]:
        """Query logs with filters.
        
        Args:
            tool_name: Filter by tool name
            status: Filter by status (success, error, running)
            start_date: Filter by start date
            end_date: Filter by end date
            limit: Maximum number of records
            
        Returns:
            List of log records as dictionaries
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        query = "SELECT * FROM tool_logs WHERE 1=1"
        params = []
        
        if tool_name:
            query += " AND tool_name = ?"
            params.append(tool_name)
        
        if status:
            query += " AND status = ?"
            params.append(status)
        
        if start_date:
            query += " AND timestamp >= ?"
            params.append(start_date.strftime("%Y-%m-%d %H:%M:%S"))
        
        if end_date:
            query += " AND timestamp <= ?"
            params.append(end_date.strftime("%Y-%m-%d %H:%M:%S"))
        
        query += " ORDER BY timestamp DESC LIMIT ?"
        params.append(limit)
        
        cursor.execute(query, params)
        columns = [desc[0] for desc in cursor.description]
        
        return [dict(zip(columns, row)) for row in cursor.fetchall()]
    
    def get_tool_stats(self) -> Dict[str, Any]:
        """Get logging statistics for dashboard.
        
        Returns:
            Dictionary with logging statistics
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        # Total logs
        cursor.execute("SELECT COUNT(*) FROM tool_logs")
        total_logs = cursor.fetchone()[0]
        
        # Success rate
        cursor.execute("""
            SELECT 
                COUNT(CASE WHEN status = 'success' THEN 1 END) as success_count,
                COUNT(CASE WHEN status = 'error' THEN 1 END) as error_count
            FROM tool_logs 
            WHERE status IN ('success', 'error')
        """)
        success_count, error_count = cursor.fetchone()
        
        # Average duration by tool
        cursor.execute("""
            SELECT tool_name, AVG(duration_ms) as avg_duration
            FROM tool_logs 
            WHERE duration_ms IS NOT NULL AND tool_name IS NOT NULL
            GROUP BY tool_name
        """)
        tool_performance = dict(cursor.fetchall())
        
        return {
            "total_logs": total_logs,
            "success_count": success_count,
            "error_count": error_count,
            "success_rate": success_count / (success_count + error_count) if (success_count + error_count) > 0 else 0,
            "tool_performance": tool_performance
        }


# Global sink instance
_sqlite_sink: Optional[SQLiteLoggerSink] = None

def initialize_sqlite_logging(config: Optional[ServerConfig] = None) -> SQLiteLoggerSink:
    """Initialize SQLite logging sink for the application.
    
    Args:
        config: Server configuration
        
    Returns:
        SQLite sink instance
    """
    global _sqlite_sink
    
    if _sqlite_sink is None:
        _sqlite_sink = SQLiteLoggerSink(config)
        
        # Add sink to loguru
        logger.add(
            _sqlite_sink,
            level="INFO",
            format="{time} | {level} | {module}:{function}:{line} | {message}",
            enqueue=True  # Thread-safe logging
        )
    
    return _sqlite_sink

def get_sqlite_sink() -> Optional[SQLiteLoggerSink]:
    """Get the global SQLite sink instance."""
    return _sqlite_sink

def log_tool_execution(tool_name: str, 
                      duration_ms: float,
                      status: str,
                      input_args: Optional[Dict[str, Any]] = None,
                      output_summary: Optional[str] = None,
                      error_message: Optional[str] = None):
    """Log MCP tool execution using Loguru with structured data.
    
    Args:
        tool_name: Name of the executed tool
        duration_ms: Execution duration in milliseconds
        status: Execution status (success, error)
        input_args: Tool input arguments
        output_summary: Summary of tool output
        error_message: Error message if status is error
    """
    logger.info(
        f"Tool {tool_name} {status} in {duration_ms:.1f}ms",
        tool_name=tool_name,
        duration_ms=duration_ms,
        status=status,
        input_args=input_args,
        output_summary=output_summary,
        error_message=error_message
    )