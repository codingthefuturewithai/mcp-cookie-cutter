"""MCP server implementation with Echo tool"""

from typing import Dict, List, Optional, Union
from mcp.server.fastmcp import FastMCP, Context
from mcp.server.stdio import stdio_server
import logging
import sys
import asyncio
import click

# Configure logging to write to stderr
logging.basicConfig(
    stream=sys.stderr,
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger("{{ cookiecutter.project_slug }}.mcp")

def create_mcp_server() -> FastMCP:
    """Create and configure the MCP server instance"""
    server = FastMCP(
        "{{ cookiecutter.project_name }}",
        host="localhost",
        port={{ cookiecutter.server_port }}
    )

    # Register all tools with the server
    register_tools(server)

    return server

def register_tools(mcp_server: FastMCP) -> None:
    """Register all MCP tools with the server"""

    @mcp_server.tool(
        name="echo",
        description="Echo back the input text",
    )
    def echo(text: str) -> str:
        """Echo the input text back to the caller"""
        return text

def run_sse_server(port: int = {{ cookiecutter.server_port }}) -> None:
    """Run the server in SSE mode using FastMCP's built-in SSE support."""
    logger.info(f"Starting SSE server on port {port}")

    # Create a new server instance for SSE
    sse_server = create_mcp_server()
    sse_server.settings.port = port

    # Run the server in SSE mode
    asyncio.run(sse_server.run_sse_async())

# Create a server instance that can be imported by the MCP CLI
server = create_mcp_server()

# Create stdio server for MCP clients
app = stdio_server(server)

@click.command()
@click.option("--port", default={{ cookiecutter.server_port }}, help="Port to listen on for SSE")
def main(port: int) -> None:
    """Run the server directly in SSE mode."""
    run_sse_server(port)

if __name__ == "__main__":
    main() 