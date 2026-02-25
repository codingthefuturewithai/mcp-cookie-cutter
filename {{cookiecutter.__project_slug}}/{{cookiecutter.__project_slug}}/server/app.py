"""{{ cookiecutter.project_name }} - MCP Server with Decorators

This module implements the core MCP server using FastMCP with multi-transport support
(STDIO, SSE, and Streamable HTTP) and automatic application of decorators
(exception handling, logging, parallelization).
"""

import asyncio
import os
import sys
from typing import Optional, Callable, Any

import click
from fastmcp import FastMCP

from {{ cookiecutter.__project_slug }}.config import ServerConfig, get_config
from {{ cookiecutter.__project_slug }}.logging_config import setup_logging, logger
from {{ cookiecutter.__project_slug }}.log_system.correlation import (
    generate_correlation_id,
    set_initialization_correlation_id,
    clear_initialization_correlation_id
)
from {{ cookiecutter.__project_slug }}.log_system.unified_logger import UnifiedLogger

from {{ cookiecutter.__project_slug }}.tools.example_tools import example_tools, parallel_example_tools


def create_mcp_server(config: Optional[ServerConfig] = None) -> FastMCP:
    """Create and configure the MCP server with decorators.
    
    Args:
        config: Optional server configuration
        
    Returns:
        Configured FastMCP server instance
    """
    if config is None:
        config = get_config()
    
    # Set startup correlation ID BEFORE initializing logging
    startup_correlation_id = "startup_" + generate_correlation_id().split('_')[1]
    set_initialization_correlation_id(startup_correlation_id)
    
    # Initialize unified logging using factory pattern
    # Convert logging_destinations dict to DestinationConfig objects
    from {{ cookiecutter.__project_slug }}.log_system.destinations import DestinationConfig
    
    destinations_list = []
    if config.logging_destinations and 'destinations' in config.logging_destinations:
        for dest_dict in config.logging_destinations['destinations']:
            dest_config = DestinationConfig(
                type=dest_dict.get('type', 'sqlite'),
                enabled=dest_dict.get('enabled', True),
                settings=dest_dict.get('settings', {})
            )
            destinations_list.append(dest_config)
    
    # Initialize with configured destinations or default to SQLite
    if destinations_list:
        UnifiedLogger.initialize_from_config(destinations_list, config)
    else:
        UnifiedLogger.initialize_default(config)
    
    # Set up traditional logging as fallback
    # IMPORTANT: This must come BEFORE UnifiedLogger.initialize to avoid overriding
    # setup_logging(config)  # Temporarily disabled to test unified logging
    
    # Log startup info using unified logger
    import logging
    unified_logger = logging.getLogger('{{ cookiecutter.__project_slug }}')
    unified_logger.info(f"Unified logging initialized with {len(UnifiedLogger.get_available_destinations())} available destination types")
    unified_logger.info(f"Server config: {config.name} at log level {config.log_level}")

    # Configure DNS rebinding protection from environment variables
    # Disabled by default for development; enable in production
    dns_protection = os.getenv("MCP_DNS_REBINDING_PROTECTION", "false").lower() == "true"
    allowed_hosts_env = os.getenv("MCP_ALLOWED_HOSTS", "")
    allowed_hosts = [h.strip() for h in allowed_hosts_env.split(",") if h.strip()] if allowed_hosts_env else []

    if dns_protection:
        unified_logger.info(f"DNS rebinding protection enabled with allowed hosts: {allowed_hosts or ['default']}")
    else:
        unified_logger.info("DNS rebinding protection disabled (development mode)")

    mcp_server = FastMCP(
        config.name or "{{ cookiecutter.project_name }}"
    )
    
    
    # Register all tools with the server
    register_tools(mcp_server, config)
    
    
    # Clear initialization correlation ID after initialization
    unified_logger.info("Server initialization complete")
    clear_initialization_correlation_id()
    
    return mcp_server



def register_tools(mcp_server: FastMCP, config: ServerConfig) -> None:
    """Register all MCP tools with the server using decorators.
    
    Registers decorated functions directly with MCP to preserve function signatures
    for proper parameter introspection.
    """
    
    # Get unified logger for registration logs
    import logging
    unified_logger = logging.getLogger('{{ cookiecutter.__project_slug }}')
    
    # Import decorators
    from {{ cookiecutter.__project_slug }}.decorators.exception_handler import exception_handler
    from {{ cookiecutter.__project_slug }}.decorators.tool_logger import tool_logger
    from {{ cookiecutter.__project_slug }}.decorators.type_converter import type_converter
    from {{ cookiecutter.__project_slug }}.decorators.parallelize import parallelize
    
    # Register regular tools with decorators
    for tool_func in example_tools:
        # Apply decorator chain: exception_handler → tool_logger → type_converter
        decorated_func = exception_handler(tool_logger(type_converter(tool_func), config.__dict__))
        
        # The decorated function preserves the original __name__
        tool_name = decorated_func.__name__
        
        # Register the decorated function with MCP using add_tool
        # The name is inferred from the function's __name__ attribute
        mcp_server.add_tool(decorated_func)
        
        unified_logger.info(f"Registered tool: {tool_name}")
    
    # Register parallel tools with decorators  
    for tool_func in parallel_example_tools:
        # Apply decorator chain: exception_handler → tool_logger → parallelize(type_converter)
        # Note: type_converter is applied to the base function before parallelize
        decorated_func = exception_handler(tool_logger(parallelize(type_converter(tool_func)), config.__dict__))
        
        # The decorated function preserves the original __name__
        tool_name = decorated_func.__name__
        
        # Register with MCP using add_tool
        mcp_server.add_tool(decorated_func)
        
        unified_logger.info(f"Registered parallel tool: {tool_name}")
    
    
    unified_logger.info(f"Server '{mcp_server.name}' initialized with decorators")


# Create a server instance that can be imported by the MCP CLI
server = create_mcp_server()


@click.command()
@click.option(
    "--port",
    default={{ cookiecutter.server_port }},
    help="Port to listen on for SSE or HTTP transport"
)
@click.option(
    "--host",
    default="127.0.0.1",
    help="Host to bind to (use 0.0.0.0 for Docker)"
)
@click.option(
    "--transport",
    type=click.Choice(["stdio", "sse", "http"]),
    default="stdio",
    help="Transport type (stdio, sse, or http)"
)
def main(port: int, host: str, transport: str) -> int:
    """Run the {{ cookiecutter.project_name }} server with specified transport."""
    try:
        if transport == "stdio":
            logger.info("Starting server with STDIO transport")
            server.run(transport="stdio")
        elif transport == "sse":
            logger.info(f"Starting server with SSE transport on {host}:{port}")
            server.run(transport="sse", host=host, port=port)
        elif transport == "http":
            logger.info(f"Starting server with HTTP transport on {host}:{port}")
            server.run(transport="http", host=host, port=port, path="/mcp")
        else:
            raise ValueError(f"Unknown transport: {transport}")
        return 0
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
        return 0
    except Exception as e:
        logger.error(f"Failed to start server: {e}", exc_info=True)
        return 1

def main_stdio() -> int:
    """Entry point for STDIO transport (convenience wrapper)."""
    import sys
    sys.argv = [sys.argv[0], "--port", "{{ cookiecutter.server_port }}", "--host", "127.0.0.1", "--transport", "stdio"] + sys.argv[1:]
    return main()

def main_http() -> int:
    """Entry point for HTTP transport (convenience wrapper)."""
    import sys
    sys.argv = [sys.argv[0], "--port", "{{ cookiecutter.server_port }}", "--host", "127.0.0.1", "--transport", "http"] + sys.argv[1:]
    return main()

def main_sse() -> int:
    """Entry point for SSE transport (convenience wrapper)."""
    import sys
    sys.argv = [sys.argv[0], "--port", "{{ cookiecutter.server_port }}", "--host", "127.0.0.1", "--transport", "sse"] + sys.argv[1:]
    return main()


if __name__ == "__main__":
    sys.exit(main())