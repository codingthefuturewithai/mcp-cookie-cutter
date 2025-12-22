"""My MCP Server - MCP Server with Decorators

This module implements the core MCP server using FastMCP with multi-transport support
(STDIO, SSE, and Streamable HTTP) and automatic application of decorators 
(exception handling, logging, parallelization).
"""

import asyncio
import sys
from typing import Optional, Callable, Any

import click
from mcp import types
from mcp.server.fastmcp import FastMCP

from my_mcp_server.config import ServerConfig, get_config
from my_mcp_server.logging_config import setup_logging, logger
from my_mcp_server.log_system.correlation import (
    generate_correlation_id,
    set_initialization_correlation_id,
    clear_initialization_correlation_id
)
from my_mcp_server.log_system.unified_logger import UnifiedLogger

from my_mcp_server.tools.example_tools import example_tools, parallel_example_tools


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
    from my_mcp_server.log_system.destinations import DestinationConfig
    
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
    unified_logger = logging.getLogger('my_mcp_server')
    unified_logger.info(f"Unified logging initialized with {len(UnifiedLogger.get_available_destinations())} available destination types")
    unified_logger.info(f"Server config: {config.name} at log level {config.log_level}")
    
    mcp_server = FastMCP(config.name or "My MCP Server")
    
    
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
    unified_logger = logging.getLogger('my_mcp_server')
    
    # Import decorators
    from my_mcp_server.decorators.exception_handler import exception_handler
    from my_mcp_server.decorators.tool_logger import tool_logger
    from my_mcp_server.decorators.type_converter import type_converter
    from my_mcp_server.decorators.parallelize import parallelize
    
    # Register regular tools with decorators
    for tool_func in example_tools:
        # Apply decorator chain: exception_handler → tool_logger → type_converter
        decorated_func = exception_handler(tool_logger(type_converter(tool_func), config.__dict__))
        
        # Extract metadata from the original function
        tool_name = tool_func.__name__
        
        # Register the decorated function directly with MCP
        # This preserves the function signature for parameter introspection
        mcp_server.tool(
            name=tool_name
        )(decorated_func)
        
        unified_logger.info(f"Registered tool: {tool_name}")
    
    # Register parallel tools with decorators  
    for tool_func in parallel_example_tools:
        # Apply decorator chain: exception_handler → tool_logger → parallelize(type_converter)
        # Note: type_converter is applied to the base function before parallelize
        decorated_func = exception_handler(tool_logger(parallelize(type_converter(tool_func)), config.__dict__))
        
        # Extract metadata
        tool_name = tool_func.__name__
        
        # Register directly with MCP
        mcp_server.tool(
            name=tool_name
        )(decorated_func)
        
        unified_logger.info(f"Registered parallel tool: {tool_name}")
    
    
    unified_logger.info(f"Server '{mcp_server.name}' initialized with decorators")


# Create a server instance that can be imported by the MCP CLI
server = create_mcp_server()


@click.command()
@click.option(
    "--port",
    default=3001,
    help="Port to listen on for SSE or Streamable HTTP transport"
)
@click.option(
    "--transport",
    type=click.Choice(["stdio", "sse", "streamable-http"]),
    default="stdio",
    help="Transport type (stdio, sse, or streamable-http)"
)
def main(port: int, transport: str) -> int:
    """Run the My MCP Server server with specified transport."""
    async def run_server():
        """Inner async function to run the server and manage the event loop."""
        # Set the event loop in UnifiedLogger for async operations
        UnifiedLogger.set_event_loop(asyncio.get_running_loop())
        
        try:
            if transport == "stdio":
                logger.info("Starting server with STDIO transport")
                await server.run_stdio_async()
            elif transport == "sse":
                logger.info(f"Starting server with SSE transport on port {port}")
                server.settings.port = port
                await server.run_sse_async()
            elif transport == "streamable-http":
                logger.info(f"Starting server with Streamable HTTP transport on port {port}")
                server.settings.port = port
                server.settings.streamable_http_path = "/mcp"
                await server.run_streamable_http_async()
            else:
                raise ValueError(f"Unknown transport: {transport}")
        finally:
            # Clean up unified logger
            await UnifiedLogger.close()
    
    try:
        asyncio.run(run_server())
        return 0
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
        return 0
    except Exception as e:
        logger.error(f"Failed to start server: {e}", exc_info=True)
        return 1

def main_stdio() -> int:
    """Entry point for STDIO transport (convenience wrapper)."""
    return main.callback(port=3001, transport="stdio")

def main_http() -> int:
    """Entry point for Streamable HTTP transport (convenience wrapper)."""
    return main.callback(port=3001, transport="streamable-http")

def main_sse() -> int:
    """Entry point for SSE transport (convenience wrapper)."""
    return main.callback(port=3001, transport="sse")


if __name__ == "__main__":
    sys.exit(main())