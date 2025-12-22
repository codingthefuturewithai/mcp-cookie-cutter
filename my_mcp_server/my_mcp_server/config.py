"""Configuration management for My MCP Server

This module provides platform-aware configuration management using platformdirs
to ensure configuration files are stored in appropriate locations across different
operating systems.
"""

import os
import yaml
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Any, Optional

import platformdirs


@dataclass
class ServerConfig:
    """Configuration class for the MCP server."""
    
    # Server settings
    name: str = "My MCP Server"
    description: str = "MCP server with decorators, unified logging, and multiple transports"
    
    # Logging configuration
    log_level: str = "INFO"
    log_retention_days: int = 30
    
    # Logging destinations configuration
    logging_destinations: Dict[str, Any] = None
    
    # Server transport settings
    default_transport: str = "stdio"
    default_host: str = "127.0.0.1"
    default_port: int = 3001
    
    # Platform-aware paths
    config_dir: Path = None
    data_dir: Path = None
    log_dir: Path = None
    
    # File paths (computed from directories)
    config_file_path: Path = None
    log_file_path: Path = None
    database_path: Path = None
    database_name: str = "unified_logs.db"
    
    def __post_init__(self):
        """Initialize platform-aware paths after dataclass creation."""
        if self.config_dir is None:
            self.config_dir = Path(platformdirs.user_config_dir("my_mcp_server"))
        if self.data_dir is None:
            self.data_dir = Path(platformdirs.user_data_dir("my_mcp_server"))
        if self.log_dir is None:
            self.log_dir = Path(platformdirs.user_log_dir("my_mcp_server"))
        
        # Ensure directories exist
        self.config_dir.mkdir(parents=True, exist_ok=True)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.log_dir.mkdir(parents=True, exist_ok=True)
        
        # Set file paths
        self.config_file_path = self.config_dir / "config.yaml"
        self.log_file_path = self.log_dir / "my_mcp_server.log"
        self.database_path = self.data_dir / self.database_name
        
        # Initialize default logging destinations if not set
        if self.logging_destinations is None:
            self.logging_destinations = {
                "destinations": [
                    {
                        "type": "sqlite",
                        "enabled": True,
                        "settings": {}
                    }
                ]
            }
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary for serialization."""
        return {
            "name": self.name,
            "description": self.description,
            "log_level": self.log_level,
            "log_retention_days": self.log_retention_days,
            "logging_destinations": self.logging_destinations,
            "default_transport": self.default_transport,
            "default_host": self.default_host,
            "default_port": self.default_port,
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ServerConfig":
        """Create configuration from dictionary (supports both flat and nested structure)."""
        # Check if data has nested structure (UI format) or flat structure (legacy)
        if "server" in data:
            # Nested structure from UI
            server_config = data.get("server", {})
            logging_config = data.get("logging", {})
            return cls(
                name=server_config.get("name", "My MCP Server"),
                description=server_config.get("description", "MCP server with decorators, unified logging, and multiple transports"),
                log_level=server_config.get("log_level", "INFO"),
                log_retention_days=logging_config.get("retention_days", 30),
                logging_destinations={"destinations": logging_config.get("destinations", [])},
                database_name=logging_config.get("database_name", "unified_logs.db"),
                default_transport=server_config.get("default_transport", "stdio"),
                default_host=server_config.get("default_host", "127.0.0.1"),
                default_port=server_config.get("port", 3001),
            )
        else:
            # Flat structure (legacy or direct from ServerConfig)
            return cls(
                name=data.get("name", "My MCP Server"),
                description=data.get("description", "MCP server with decorators, unified logging, and multiple transports"),
                log_level=data.get("log_level", "INFO"),
                log_retention_days=data.get("log_retention_days", 30),
                logging_destinations=data.get("logging_destinations"),
                database_name=data.get("database_name", "unified_logs.db"),
                default_transport=data.get("default_transport", "stdio"),
                default_host=data.get("default_host", "127.0.0.1"),
                default_port=data.get("default_port", 3001),
            )
    
    def save(self) -> None:
        """Save configuration to file in nested structure for UI compatibility."""
        try:
            # Convert to nested structure for UI
            nested_config = {
                "server": {
                    "name": self.name,
                    "description": self.description,
                    "port": self.default_port,
                    "log_level": self.log_level,
                    "default_transport": self.default_transport,
                    "default_host": self.default_host
                },
                "logging": {
                    "level": self.log_level,
                    "retention_days": self.log_retention_days,
                    "database_name": self.database_name,
                    "destinations": self.logging_destinations.get("destinations", []) if self.logging_destinations else []
                }
            }
            with open(self.config_file_path, 'w') as f:
                yaml.dump(nested_config, f, default_flow_style=False)
        except Exception as e:
            print(f"Warning: Could not save configuration: {e}")
    
    @classmethod
    def load(cls) -> "ServerConfig":
        """Load configuration from file, creating default if not found."""
        config = cls()  # Create with defaults
        
        if config.config_file_path.exists():
            try:
                with open(config.config_file_path, 'r') as f:
                    data = yaml.safe_load(f)
                    if data:
                        # Update with loaded values
                        loaded_config = cls.from_dict(data)
                        # Preserve the paths from the original config
                        loaded_config.config_dir = config.config_dir
                        loaded_config.data_dir = config.data_dir
                        loaded_config.log_dir = config.log_dir
                        loaded_config.config_file_path = config.config_file_path
                        loaded_config.log_file_path = config.log_file_path
                        loaded_config.database_path = config.database_path
                        return loaded_config
            except Exception as e:
                print(f"Warning: Could not load configuration: {e}")
        
        # Save default configuration
        config.save()
        return config
    
    def __str__(self) -> str:
        """String representation of configuration."""
        return f"ServerConfig(name='{self.name}', log_level='{self.log_level}', transport='{self.default_transport}')"


# Global configuration instance
_config: Optional[ServerConfig] = None


def get_config() -> ServerConfig:
    """Get the global configuration instance, loading it if necessary."""
    global _config
    if _config is None:
        _config = ServerConfig.load()
    return _config


def reload_config() -> ServerConfig:
    """Reload configuration from file."""
    global _config
    _config = ServerConfig.load()
    return _config


def get_platform_info() -> Dict[str, str]:
    """Get platform-specific directory information."""
    return {
        "config_dir": str(platformdirs.user_config_dir("my_mcp_server")),
        "data_dir": str(platformdirs.user_data_dir("my_mcp_server")),
        "log_dir": str(platformdirs.user_log_dir("my_mcp_server")),
        "cache_dir": str(platformdirs.user_cache_dir("my_mcp_server")),
    }


# Backward compatibility
def load_config() -> ServerConfig:
    """Load server configuration from environment or defaults (backward compatibility)"""
    return get_config()


if __name__ == "__main__":
    # Test configuration loading
    config = get_config()
    print(f"Configuration loaded: {config}")
    print(f"Platform info: {get_platform_info()}")
    print(f"Config file: {config.config_file_path}")
    print(f"Log file: {config.log_file_path}")
    print(f"Database: {config.database_path}")