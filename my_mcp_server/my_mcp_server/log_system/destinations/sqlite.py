"""
SQLite implementation of the LogDestination interface.

This module provides a SQLite-based logging destination that stores unified
logs in a local database with thread-safe access and connection pooling.
"""

import json
import sqlite3
import threading
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional

from ..destinations.base import LogDestination, LogEntry
from my_mcp_server.config import ServerConfig


class SQLiteDestination(LogDestination):
    """SQLite implementation of LogDestination.
    
    This class provides thread-safe SQLite storage for unified logs with
    connection pooling and automatic schema creation.
    """
    
    def __init__(self, config: ServerConfig):
        """Initialize the SQLite destination.
        
        Args:
            config: Server configuration containing database path
        """
        self.config = config
        self._db_path = self._get_database_path()
        self._local = threading.local()
        self._initialize_database()
    
    def _get_database_path(self) -> Path:
        """Get the database path from config, creating directories if needed."""
        # Use unified_logs.db instead of the main database
        db_path = self.config.data_dir / "unified_logs.db"
        db_path.parent.mkdir(parents=True, exist_ok=True)
        return db_path
    
    def _get_connection(self) -> sqlite3.Connection:
        """Get a thread-local database connection."""
        if not hasattr(self._local, 'connection') or self._local.connection is None:
            self._local.connection = sqlite3.connect(
                str(self._db_path),
                check_same_thread=False,
                timeout=30.0
            )
            self._local.connection.row_factory = sqlite3.Row
            # Enable foreign keys
            self._local.connection.execute("PRAGMA foreign_keys = ON")
            # Try WAL mode for better concurrency, but fall back if it fails (Windows file locking)
            try:
                self._local.connection.execute("PRAGMA journal_mode = WAL")
            except sqlite3.OperationalError:
                # Fall back to DELETE mode if WAL fails (common on Windows with certain file systems)
                self._local.connection.execute("PRAGMA journal_mode = DELETE")
        return self._local.connection
    
    def _initialize_database(self) -> None:
        """Initialize the database schema."""
        conn = self._get_connection()
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS unified_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                correlation_id TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                level TEXT NOT NULL,
                log_type TEXT CHECK(log_type IN ('tool_execution', 'internal', 'framework')),
                message TEXT NOT NULL,
                tool_name TEXT,
                duration_ms REAL,
                status TEXT CHECK(status IN ('success', 'error', 'running', NULL)),
                input_args TEXT,  -- JSON
                output_summary TEXT,
                error_message TEXT,
                module TEXT,
                function TEXT,
                line INTEGER,
                thread_name TEXT,
                process_id INTEGER,
                extra_data TEXT,  -- JSON
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            );
            
            -- Indexes for performance
            CREATE INDEX IF NOT EXISTS idx_correlation_id ON unified_logs(correlation_id);
            CREATE INDEX IF NOT EXISTS idx_timestamp ON unified_logs(timestamp);
            CREATE INDEX IF NOT EXISTS idx_level ON unified_logs(level);
            CREATE INDEX IF NOT EXISTS idx_tool_name ON unified_logs(tool_name);
            CREATE INDEX IF NOT EXISTS idx_log_type ON unified_logs(log_type);
        """)
        conn.commit()
    
    def write_sync(self, entry: LogEntry) -> None:
        """Write a log entry to SQLite synchronously.
        
        Args:
            entry: The log entry to write
        """
        conn = self._get_connection()
        
        # Serialize complex fields to JSON
        input_args_json = json.dumps(entry.input_args) if entry.input_args else None
        extra_data_json = json.dumps(entry.extra_data) if entry.extra_data else None
        
        # Convert timestamp to string format for SQLite
        timestamp_str = entry.timestamp.isoformat() if isinstance(entry.timestamp, datetime) else str(entry.timestamp)
        
        conn.execute("""
            INSERT INTO unified_logs (
                correlation_id, timestamp, level, log_type, message,
                tool_name, duration_ms, status, input_args, output_summary,
                error_message, module, function, line, thread_name,
                process_id, extra_data
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            entry.correlation_id,
            timestamp_str,
            entry.level,
            entry.log_type,
            entry.message,
            entry.tool_name,
            entry.duration_ms,
            entry.status,
            input_args_json,
            entry.output_summary,
            entry.error_message,
            entry.module,
            entry.function,
            entry.line,
            entry.thread_name,
            entry.process_id,
            extra_data_json
        ))
        conn.commit()
    
    async def write(self, entry: LogEntry) -> None:
        """Write a log entry to SQLite (async wrapper for compatibility).
        
        Args:
            entry: The log entry to write
        """
        # SQLite operations are synchronous anyway, so just call the sync version
        self.write_sync(entry)
    
    async def query(self, **filters) -> List[LogEntry]:
        """Query logs with filters.
        
        Supported filters:
        - correlation_id: str
        - tool_name: str
        - level: str
        - log_type: str
        - start_time: datetime
        - end_time: datetime
        - limit: int (default 1000)
        
        Args:
            **filters: Keyword arguments for filtering
            
        Returns:
            List of matching log entries
        """
        conn = self._get_connection()
        
        # Build query
        query = "SELECT * FROM unified_logs WHERE 1=1"
        params = []
        
        if 'correlation_id' in filters:
            query += " AND correlation_id = ?"
            params.append(filters['correlation_id'])
        
        if 'tool_name' in filters:
            query += " AND tool_name = ?"
            params.append(filters['tool_name'])
        
        if 'level' in filters:
            query += " AND level = ?"
            params.append(filters['level'])
        
        if 'log_type' in filters:
            query += " AND log_type = ?"
            params.append(filters['log_type'])
        
        if 'start_time' in filters:
            query += " AND timestamp >= ?"
            start_time = filters['start_time']
            if isinstance(start_time, datetime):
                params.append(start_time.isoformat())
            else:
                params.append(str(start_time))
        
        if 'end_time' in filters:
            query += " AND timestamp <= ?"
            end_time = filters['end_time']
            if isinstance(end_time, datetime):
                params.append(end_time.isoformat())
            else:
                params.append(str(end_time))
        
        # Order by timestamp descending
        query += " ORDER BY timestamp DESC"
        
        # Apply limit
        limit = filters.get('limit', 1000)
        query += f" LIMIT {limit}"
        
        cursor = conn.execute(query, params)
        entries = []
        
        for row in cursor:
            # Parse JSON fields
            input_args = json.loads(row['input_args']) if row['input_args'] else None
            extra_data = json.loads(row['extra_data']) if row['extra_data'] else {}
            
            # Parse timestamp
            timestamp = datetime.fromisoformat(row['timestamp']) if row['timestamp'] else datetime.now()
            
            entry = LogEntry(
                correlation_id=row['correlation_id'],
                timestamp=timestamp,
                level=row['level'],
                log_type=row['log_type'],
                message=row['message'],
                tool_name=row['tool_name'],
                duration_ms=row['duration_ms'],
                status=row['status'],
                input_args=input_args,
                output_summary=row['output_summary'],
                error_message=row['error_message'],
                module=row['module'],
                function=row['function'],
                line=row['line'],
                thread_name=row['thread_name'],
                process_id=row['process_id'],
                extra_data=extra_data
            )
            entries.append(entry)
        
        return entries
    
    async def close(self) -> None:
        """Close the database connection."""
        if hasattr(self._local, 'connection') and self._local.connection:
            self._local.connection.close()
            self._local.connection = None