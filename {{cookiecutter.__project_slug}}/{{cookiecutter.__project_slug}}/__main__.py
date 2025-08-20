"""Main module for {{cookiecutter.project_name}} MCP server.

This module allows the server to be run as a Python module using:
python -m {{cookiecutter.__project_slug}}

It delegates to the server application's main function.
"""

from {{ cookiecutter.__project_slug }}.server.app import main

if __name__ == "__main__":
    main()