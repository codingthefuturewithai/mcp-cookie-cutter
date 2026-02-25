"""Exception handling decorator for MCP tools.

This decorator provides graceful error handling:
- Async-only pattern
- Standard error response format
- Full traceback preservation
- Integration with logging system

Features:
- Automatic exception catching and logging
- Graceful error recovery with fallback responses
- Standard error messages
- Full traceback preservation for debugging
- Async-only pattern for consistency

Usage:
    @exception_handler
    async def my_tool(param: str) -> str:
        # Tool implementation
        return result
"""

import asyncio
from functools import wraps
from typing import Callable, Any, Awaitable
import logging
import traceback
from {{ cookiecutter.__project_slug }}.log_system.unified_logger import UnifiedLogger
from {{ cookiecutter.__project_slug }}.log_system.correlation import get_correlation_id


def exception_handler(func: Callable[..., Awaitable[Any]]) -> Callable[..., Awaitable[Any]]:
    """Decorator to handle exceptions in MCP tools gracefully.
    
    Preserves function signature for MCP introspection while adding
    exception handling capabilities. Async-only pattern.
    
    Args:
        func: The async function to decorate
        
    Returns:
        The decorated async function with exception handling
    """
    
    @wraps(func)
    async def wrapper(*args, **kwargs) -> Any:
        try:
            return await func(*args, **kwargs)
        except Exception as e:
            # Get correlation-aware logger with tool name
            logger = UnifiedLogger.get_logger(f"tool.{func.__name__}")
            
            # Log the full traceback for debugging
            tb_str = traceback.format_exc()
            # Escape { } so loguru doesn't interpret source code like
            # {variable_name} in tracebacks as format placeholders
            {% raw %}
            safe_tb = tb_str.replace("{", "{{").replace("}", "}}")
            {% endraw %}
            logger.error(
                f"Exception in {func.__name__}: {safe_tb}",
                log_type="tool_execution",
                tool_name=func.__name__,
                status="error",
                error_message=str(e),
                exception_type=type(e).__name__
            )
            
            # Re-raise the exception for MCP to handle properly
            # This ensures MCP returns a proper error response to the client
            raise
    
    return wrapper