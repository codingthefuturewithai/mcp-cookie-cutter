"""MCP server package initialization"""

from my_mcp_server.config import load_config
from my_mcp_server.server.app import create_mcp_server

# Create server instance with default configuration
server = create_mcp_server(load_config())

__all__ = ["server", "create_mcp_server"]
