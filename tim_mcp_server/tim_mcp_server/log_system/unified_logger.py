"""
Unified logging factory with Loguru integration.

This module provides a factory for creating correlation-aware loggers that
write to pluggable destinations while intercepting both Loguru and standard
Python logging.
"""

import logging
import sys
import asyncio
from typing import Optional, Any, Dict, List
from datetime import datetime

from loguru import logger

from .correlation import get_correlation_id, get_initialization_correlation_id
from .destinations.base import LogDestination, LogEntry
from .destinations.factory import LogDestinationFactory, DestinationConfig
from .destinations.sqlite import SQLiteDestination


class UnifiedLogger:
    """Factory for creating correlation-aware loggers with pluggable destinations."""
    
    _destination: Optional[LogDestination] = None
    _initialized: bool = False
    _event_loop: Optional[asyncio.AbstractEventLoop] = None
    
    @classmethod
    def initialize(cls, destination: LogDestination, event_loop: Optional[asyncio.AbstractEventLoop] = None):
        """Initialize the unified logging system with a specific destination.
        
        Args:
            destination: The LogDestination implementation to use
            event_loop: Optional event loop for async operations. If not provided,
                       will attempt to get the current running loop when needed.
        """
        if cls._initialized:
            # Clean up previous configuration
            logger.remove()
        
        cls._destination = destination
        cls._event_loop = event_loop
        cls._initialized = True
        
        # Remove default Loguru handler
        logger.remove()
        
        # Add custom sink that writes to destination
        logger.add(
            cls._log_sink,
            level="DEBUG",
            enqueue=True,  # Thread-safe enqueueing
            serialize=False  # We'll handle serialization ourselves
        )
        
        # Configure standard library logging to use Loguru
        logging.basicConfig(handlers=[InterceptHandler()], level=logging.INFO, force=True)
        
        # Silence noisy loggers
        logging.getLogger('asyncio').setLevel(logging.WARNING)
        logging.getLogger('asyncio.selector_events').setLevel(logging.WARNING)
        
        # Also intercept root logger
        logging.getLogger().handlers = [InterceptHandler()]
    
    @classmethod
    def _log_sink(cls, message):
        """Custom Loguru sink that writes to the configured destination.
        
        This method is called by Loguru for each log message and converts
        it to our unified LogEntry format before writing to the destination.
        """
        if not cls._destination:
            return
        
        record = message.record
        
        # Extract extra data
        extra = dict(record["extra"])
        
        # Build LogEntry
        # Get correlation ID from the bound logger context, not current context
        entry = LogEntry(
            correlation_id=extra.get("correlation_id") or get_correlation_id() or get_initialization_correlation_id() or "init",
            timestamp=record["time"].replace(tzinfo=None),  # Remove timezone for SQLite
            level=record["level"].name,
            log_type=extra.get("log_type", "internal"),
            message=str(record["message"]),
            tool_name=extra.get("tool_name"),
            duration_ms=extra.get("duration_ms"),
            status=extra.get("status"),
            input_args=extra.get("input_args"),
            output_summary=extra.get("output_summary"),
            error_message=extra.get("error_message"),
            module=record["module"],
            function=record["function"],
            line=record["line"],
            thread_name=record["thread"].name if record["thread"] else None,
            process_id=record["process"].id if record["process"] else None,
            extra_data={k: v for k, v in extra.items() 
                       if k not in ["log_type", "tool_name", "duration_ms", "status",
                                   "input_args", "output_summary", "error_message"]}
        )
        
        # Write to destination
        # SQLiteDestination has both sync and async write methods
        # Always use the sync method since SQLite operations are synchronous anyway
        if hasattr(cls._destination, 'write_sync'):
            # SQLite destination - use sync write directly
            try:
                cls._destination.write_sync(entry)
            except Exception as e:
                import sys
                print(f"Warning: Could not write log entry: {e}", file=sys.stderr)
        else:
            # Other destinations that might be truly async
            try:
                loop = cls._event_loop
                if not loop:
                    try:
                        loop = asyncio.get_running_loop()
                    except RuntimeError:
                        loop = None
                
                if loop and loop.is_running():
                    # We're in an async context with a running loop
                    asyncio.create_task(cls._destination.write(entry))
                else:
                    # We're in a sync context or no loop is running
                    asyncio.run(cls._destination.write(entry))
            except Exception as e:
                import sys
                print(f"Warning: Could not write log entry: {e}", file=sys.stderr)
    
    @classmethod
    def get_logger(cls, name: Optional[str] = None):
        """Get a correlation-aware logger instance.
        
        Args:
            name: Optional logger name for identification
            
        Returns:
            A Loguru logger instance bound with correlation ID and name
        """
        bindings = {
            "correlation_id": get_correlation_id()
        }
        
        if name:
            bindings["logger_name"] = name
        
        return logger.bind(**bindings)
    
    @classmethod
    def set_event_loop(cls, loop: asyncio.AbstractEventLoop):
        """Set the event loop for async operations.
        
        This should be called when the application starts its event loop.
        """
        cls._event_loop = loop
    
    @classmethod
    async def close(cls):
        """Close the logging system and clean up resources."""
        if cls._destination:
            await cls._destination.close()
            cls._destination = None
        cls._initialized = False
        logger.remove()
    
    @classmethod
    def initialize_from_config(cls, destinations_config: List[DestinationConfig], server_config, event_loop: Optional[asyncio.AbstractEventLoop] = None):
        """Initialize the unified logging system from configuration.
        
        This method uses the factory pattern to create destinations based on configuration.
        
        Args:
            destinations_config: List of DestinationConfig objects
            server_config: Server configuration object
            event_loop: Optional event loop for async operations
        """
        destination = LogDestinationFactory.create_from_config(destinations_config, server_config)
        cls.initialize(destination, event_loop)
    
    @classmethod
    def initialize_default(cls, server_config, event_loop: Optional[asyncio.AbstractEventLoop] = None):
        """Initialize with default SQLite destination for backward compatibility.
        
        Args:
            server_config: Server configuration object
            event_loop: Optional event loop for async operations
        """
        # Create a default SQLite configuration
        default_config = [DestinationConfig(type='sqlite', enabled=True)]
        destination = LogDestinationFactory.create_from_config(default_config, server_config)
        cls.initialize(destination, event_loop)
    
    @classmethod
    def get_available_destinations(cls) -> List[str]:
        """Get list of available destination types.
        
        Returns:
            List of registered destination type names
        """
        return LogDestinationFactory.get_available_types()


class InterceptHandler(logging.Handler):
    """Intercept standard library logging and route to Loguru.
    
    This handler captures all standard logging calls and forwards them
    to Loguru, preserving the original context and level information.
    """
    
    def emit(self, record: logging.LogRecord):
        """Emit a log record by forwarding to Loguru."""
        # Get corresponding Loguru level if it exists
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno
        
        # Find caller from where originated the logged message
        frame, depth = sys._getframe(6), 6
        while frame and frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1
        
        # Log with Loguru, preserving the original context
        logger.opt(depth=depth, exception=record.exc_info).log(
            level,
            record.getMessage()
        )