"""MCP server implementation with Echo tool"""

from mcp.server.fastmcp import FastMCP
from mcp import types
import logging
import sys
import asyncio
import click
from typing import Optional

from {{cookiecutter.project_slug}}.tools.echo import echo

# Configure logging to write to stderr
logging.basicConfig(
    stream=sys.stderr,
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger("{{cookiecutter.project_slug}}.mcp")

def create_mcp_server() -> FastMCP:
    """Create and configure the MCP server instance"""
    server = FastMCP(
        "{{cookiecutter.project_name}}",
        host="localhost",
        port={{cookiecutter.server_port}}
    )

    # Register all tools with the server
    register_tools(server)

    return server

def register_tools(mcp_server: FastMCP) -> None:
    """Register all MCP tools with the server"""
    @mcp_server.tool(
        name="echo",
        description="Echo back the input text with optional case transformation",
    )
    def echo_tool(text: str, transform: Optional[str] = None) -> types.TextContent:
        """Wrapper around the echo tool implementation"""
        return echo(text, transform)

# Create a server instance that can be imported by the MCP CLI
server = create_mcp_server()

@click.command()
@click.option("--port", default={{cookiecutter.server_port}}, help="Port to listen on for SSE")
@click.option(
    "--transport",
    type=click.Choice(["stdio", "sse"]),
    default="stdio",
    help="Transport type (stdio or sse)",
)
def main(port: int, transport: str) -> int:
    """Run the server with specified transport."""
    try:
        if transport == "stdio":
            asyncio.run(server.run_stdio_async())
        else:
            server.settings.port = port
            asyncio.run(server.run_sse_async())
        return 0
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
        return 0
    except Exception as e:
        logger.error(f"Failed to start server: {e}", exc_info=True)
        return 1

if __name__ == "__main__":
    sys.exit(main()) 