"""MCP server package initialization"""

from {{cookiecutter.__project_slug}}.config import load_config
from {{cookiecutter.__project_slug}}.server.app import create_mcp_server

# Create server instance with default configuration
server = create_mcp_server(load_config())

__all__ = ["server", "create_mcp_server"]
