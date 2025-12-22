"""Main module for My MCP Server MCP server.

This module allows the server to be run as a Python module using:
python -m my_mcp_server

It delegates to the server application's main function.
"""

from my_mcp_server.server.app import main

if __name__ == "__main__":
    main()