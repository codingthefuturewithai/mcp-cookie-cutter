"""
Unified logging system for My MCP Server.

This module provides a pluggable logging architecture with correlation IDs
for tracking related events across tool executions and internal logs.

Example usage for tool developers:
    from my_mcp_server.log_system import get_tool_logger
    
    async def my_custom_tool(param: str) -> str:
        logger = get_tool_logger("my_custom_tool")
        
        logger.debug(f"Received parameter: {param}")
        
        try:
            # Tool logic
            result = process_data(param)
            logger.info(f"Successfully processed data")
            return result
        except Exception as e:
            logger.error(f"Failed to process: {e}")
            raise
"""

from .unified_logger import UnifiedLogger
from .correlation import get_correlation_id, set_correlation_id, CorrelationContext
from .destinations import LogDestination, LogEntry, SQLiteDestination


def get_tool_logger(tool_name: str):
    """Get a logger for tool developers that automatically includes correlation ID.
    
    This logger will automatically include the current correlation ID in all
    log messages, making it easy to track related events across the system.
    
    Args:
        tool_name: Name of the tool for identification in logs
        
    Returns:
        A correlation-aware logger instance
        
    Example:
        logger = get_tool_logger("my_tool")
        logger.info("Processing started")
    """
    return UnifiedLogger.get_logger(f"tool.{tool_name}")


# Export public API
__all__ = [
    "get_tool_logger",
    "get_correlation_id",
    "set_correlation_id",
    "CorrelationContext",
    "LogDestination",
    "LogEntry",
    "SQLiteDestination",
    "UnifiedLogger"
]