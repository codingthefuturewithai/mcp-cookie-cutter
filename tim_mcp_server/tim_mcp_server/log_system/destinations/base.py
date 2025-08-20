"""
Base classes for logging destinations.

This module defines the abstract interface for pluggable logging destinations
and the unified log entry structure used across all destinations.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class LogEntry:
    """Unified log entry structure for all destinations."""
    correlation_id: str
    timestamp: datetime
    level: str
    log_type: str  # 'tool_execution', 'internal', 'framework'
    message: str
    tool_name: Optional[str] = None
    duration_ms: Optional[float] = None
    status: Optional[str] = None
    input_args: Optional[Dict[str, Any]] = None
    output_summary: Optional[str] = None
    error_message: Optional[str] = None
    module: Optional[str] = None
    function: Optional[str] = None
    line: Optional[int] = None
    thread_name: Optional[str] = None
    process_id: Optional[int] = None
    extra_data: Optional[Dict[str, Any]] = field(default_factory=dict)


@dataclass
class DestinationConfig:
    """Configuration for a log destination."""
    type: str
    enabled: bool = True
    settings: Dict[str, Any] = field(default_factory=dict)


class LogDestination(ABC):
    """Abstract base class for all log destinations.
    
    This interface defines the contract that all logging destinations must
    implement to support pluggable logging backends. Implementations should
    handle their own resource management, connection pooling, and error handling.
    """
    
    @abstractmethod
    async def write(self, entry: LogEntry) -> None:
        """Write a log entry to the destination.
        
        Args:
            entry: The log entry to write
            
        Raises:
            Exception: If the write operation fails
        """
        pass
    
    @abstractmethod
    async def query(self, **filters) -> List[LogEntry]:
        """Query logs with filters.
        
        Supported filters may vary by implementation but should include:
        - correlation_id: str
        - tool_name: str
        - level: str
        - log_type: str
        - start_time: datetime
        - end_time: datetime
        - limit: int
        
        Args:
            **filters: Keyword arguments for filtering
            
        Returns:
            List of matching log entries
        """
        pass
    
    @abstractmethod
    async def close(self) -> None:
        """Clean up resources.
        
        This method should close connections, flush buffers, and perform
        any other cleanup necessary when shutting down the logging system.
        """
        pass
    
    async def __aenter__(self):
        """Async context manager entry."""
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.close()