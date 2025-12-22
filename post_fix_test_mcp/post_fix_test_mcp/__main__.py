"""Main module for Post-fix Test MCP MCP server.

This module allows the server to be run as a Python module using:
python -m post_fix_test_mcp

It delegates to the server application's main function.
"""

from post_fix_test_mcp.server.app import main

if __name__ == "__main__":
    main()