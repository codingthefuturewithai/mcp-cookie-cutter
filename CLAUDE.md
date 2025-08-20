# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Python Cookiecutter template for creating MCP (Model Context Protocol) servers. MCP enables AI assistants to interact with external tools and services through a standardized protocol.

## Key Commands

### Template Development
```bash
# Create a new project from this template
cookiecutter .

# Install template dependencies (for development)
cd {{cookiecutter.__project_slug}}
uv pip install -e .
```

### Generated Project Commands
```bash
# Test with stdio transport (default)
{{cookiecutter.__project_slug}}-client "Hello, World"

# Test with SSE transport
{{cookiecutter.__project_slug}}-server --transport sse --port 3001

# Test with MCP Inspector
mcp dev {{cookiecutter.__project_slug}}/server/app.py

# Build distribution
python -m build --wheel
```

## Architecture

The template generates projects with this structure:
- `server/app.py`: Unified MCP server supporting both stdio and SSE transports
- `client/app.py`: Test client for development (stdio only)
- `tools/`: Directory for tool implementations (business logic)
- `config.py`: Runtime configuration management
- `logging_config.py`: OS-specific logging setup with file rotation

### Key Design Patterns

1. **Unified Transport Handling**: Single server codebase supports multiple transports via command-line arguments
2. **Tool Registration**: Tools are implemented separately and registered with the server
3. **Absolute Imports**: All imports use the full package path (e.g., `from {{cookiecutter.__project_slug}}.tools.echo import ...`)

### Adding New Tools

1. Create a new file in `tools/` directory
2. Implement tool functions following the pattern in `tools/echo.py`
3. Register the tool in `server/app.py` using `@mcp.tool()`

## Important Configuration

- Python 3.11-3.13 required
- Main dependencies: `mcp`, `anyio`, `starlette`, `uvicorn`
- Default SSE port: 3001 (configurable)
- Logging: Writes to OS-specific locations with 10MB rotation

## MCP-Specific Notes

- The server supports both stdio (for direct integration) and SSE (for HTTP-based access) transports
- Tools must handle various content types: Text, Image, JSON, File, Binary
- Use MCP Inspector for interactive development and testing
- The protocol requires proper error handling and response formatting