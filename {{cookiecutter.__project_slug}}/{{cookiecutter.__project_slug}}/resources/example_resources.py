"""Example MCP resources for {{ cookiecutter.project_name }}

Resources expose read-only data to MCP clients, addressed by URI. Unlike
tools (model-controlled actions), resources are application-controlled
context: the host decides when to read them and how to surface them.

Two patterns are demonstrated:
1. Static resource     - a fixed URI (config://server)
2. Resource template   - a parameterized URI (greeting://{name})

Add your own resources here and they will be registered by
register_resources() in server/app.py.
"""

import json

from mcp.server.fastmcp import FastMCP

from {{ cookiecutter.__project_slug }}.config import get_config
from {{ cookiecutter.__project_slug }}.log_system.unified_logger import UnifiedLogger


def register_resources(mcp_server: FastMCP) -> None:
    """Register all example resources with the MCP server."""

    @mcp_server.resource(
        "config://server",
        title="Server Configuration",
        description="Current server configuration (non-sensitive fields)",
        mime_type="application/json",
    )
    def server_config() -> str:
        """Expose non-sensitive server configuration as JSON."""
        logger = UnifiedLogger.get_logger(__name__)
        logger.info("Resource read: config://server")
        config = get_config()
        return json.dumps(
            {
                "name": config.name,
                "log_level": config.log_level,
            },
            indent=2,
        )

    @mcp_server.resource(
        "greeting://{name}",
        title="Personalized Greeting",
        description="A personalized greeting for the given name",
        mime_type="text/plain",
    )
    def greeting(name: str) -> str:
        """Resource template: URI parameters map to function arguments."""
        logger = UnifiedLogger.get_logger(__name__)
        logger.info(f"Resource read: greeting://{name}")
        return f"Hello, {name}! Welcome to {{ cookiecutter.project_name }}."
