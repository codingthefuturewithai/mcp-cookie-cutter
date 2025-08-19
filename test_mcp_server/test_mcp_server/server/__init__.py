"""MCP server package initialization"""

from test_mcp_server.config import load_config
from test_mcp_server.server.app import create_mcp_server

# Create server instance with default configuration
server = create_mcp_server(load_config())

__all__ = ["server", "create_mcp_server"]
