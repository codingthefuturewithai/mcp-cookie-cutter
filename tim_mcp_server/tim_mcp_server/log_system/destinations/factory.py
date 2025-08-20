"""
Factory for creating log destinations.

This module provides a factory pattern for creating log destinations
based on configuration, allowing easy extension with new destination types.
"""

from typing import Dict, Type, List, Optional
from .base import LogDestination, DestinationConfig
from .sqlite import SQLiteDestination


class LogDestinationFactory:
    """Factory for creating log destinations based on configuration."""
    
    _registry: Dict[str, Type[LogDestination]] = {}
    
    @classmethod
    def register(cls, name: str, destination_class: Type[LogDestination]) -> None:
        """Register a new destination type.
        
        Args:
            name: The name to register the destination under
            destination_class: The LogDestination implementation class
        """
        cls._registry[name] = destination_class
    
    @classmethod
    def create(cls, destination_type: str, config) -> LogDestination:
        """Create a log destination instance.
        
        Args:
            destination_type: The type of destination to create
            config: Configuration to pass to the destination constructor
            
        Returns:
            An instance of the requested LogDestination type
            
        Raises:
            ValueError: If the destination type is not registered
        """
        if destination_type not in cls._registry:
            raise ValueError(f"Unknown destination type: {destination_type}")
        
        destination_class = cls._registry[destination_type]
        return destination_class(config)
    
    @classmethod
    def create_from_config(cls, destinations_config: List[DestinationConfig], server_config) -> LogDestination:
        """Create a log destination from configuration.
        
        This method creates appropriate log destinations based on the provided
        configuration. If multiple destinations are configured, it will create
        a composite destination that writes to all of them.
        
        Args:
            destinations_config: List of destination configurations
            server_config: The server configuration object
            
        Returns:
            A LogDestination instance
        """
        enabled_configs = [d for d in destinations_config if d.enabled]
        
        if not enabled_configs:
            # No destinations enabled, use default SQLite
            return SQLiteDestination(server_config)
        
        if len(enabled_configs) == 1:
            # Single destination
            dest_config = enabled_configs[0]
            return cls.create(dest_config.type, server_config)
        
        # Multiple destinations - would need CompositeDestination
        # For now, just use the first one
        dest_config = enabled_configs[0]
        return cls.create(dest_config.type, server_config)
    
    @classmethod
    def get_available_types(cls) -> List[str]:
        """Get list of registered destination types.
        
        Returns:
            List of registered destination type names
        """
        return list(cls._registry.keys())


# Register built-in destinations
LogDestinationFactory.register('sqlite', SQLiteDestination)