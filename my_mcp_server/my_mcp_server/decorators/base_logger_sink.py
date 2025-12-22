"""Base logger sink abstract class for MCP tool logging.

This module provides the abstract base class that all logger sinks must inherit from.
It ensures consistent interface across different logging destinations (SQLite, file, cloud, etc.)
and provides common functionality like log location retrieval.

Features:
- Abstract base class defining logger sink interface
- Required methods for all logger implementations
- Consistent log location retrieval across all sinks
"""

from abc import ABC, abstractmethod
from typing import Optional
from my_mcp_server.config import ServerConfig


class BaseLoggerSink(ABC):
    """Abstract base class for all logger sink implementations.
    
    All logger sinks (SQLite, file-based, cloud-based, etc.) must inherit
    from this class and implement the required abstract methods.
    """
    
    def __init__(self, config: Optional[ServerConfig] = None):
        """Initialize the base logger sink.
        
        Args:
            config: Server configuration for the logger
        """
        self.config = config or ServerConfig()
    
    @abstractmethod
    def get_log_location(self) -> str:
        """Get the location where logs are stored.
        
        This method must return a string describing where logs can be found.
        For file-based loggers, this would be a file path. For cloud loggers,
        this might be a URL or resource identifier.
        
        Returns:
            String describing the log location
        """
        pass
    
    @abstractmethod
    def __call__(self, message):
        """Process a log message.
        
        This method is called by Loguru for each log record. Implementations
        should handle the message according to their specific storage mechanism.
        
        Args:
            message: Loguru message object with record data
        """
        pass
    
    def cleanup_old_logs(self):
        """Remove logs older than retention period.
        
        This is an optional method that implementations can override to provide
        log cleanup functionality. Default implementation does nothing.
        """
        pass