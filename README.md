# MCP Server Cookie Cutter Template

A cookie cutter template for creating new MCP (Machine Control Protocol) servers. This template generates a fully functional MCP server with unified transport handling (stdio and SSE) and MCP Inspector compatibility, demonstrated through a simple echo service.

## Features

- Unified transport handling (stdio and SSE in a single implementation)
- Full MCP Inspector compatibility
- Example echo tool implementation
- Proper absolute imports throughout
- Development environment setup
- Comprehensive documentation templates

## Prerequisites

1. Python 3.11 or higher

   ```bash
   python --version  # Should be 3.11 or higher
   ```

2. uv (Fast Python package installer)

   ```bash
   # Install uv if you don't have it
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

3. Cookie Cutter
   ```bash
   uv pip install cookiecutter
   ```

## Creating a New MCP Server

You can create a new MCP server either directly from GitHub or from a local copy of this template.

### Option 1: Directly from GitHub

```bash
cookiecutter gh:codingthefuturewithai/mcp-cookie-cutter
```

### Option 2: From Local Copy

1. Clone this template:

   ```bash
   git clone https://github.com/codingthefuturewithai/mcp-cookie-cutter
   ```

2. Create a project using the local template:
   ```bash
   cookiecutter path/to/mcp-cookie-cutter
   ```

### Template Configuration

You'll be asked for:

- `project_name`: Human-readable name (e.g., "My MCP Server")
- `project_slug`: Python package name (e.g., "my_mcp_server")
- `description`: Short description of your project
- `author_name`: Your name
- `author_email`: Your email
- `server_port`: Port for SSE server (default: 3001)

## Generated Project Structure

```
my_mcp_server/              # Your project directory
├── my_mcp_server/          # Python package directory
│   ├── __init__.py
│   ├── client/             # Client implementations
│   │   ├── __init__.py
│   │   └── app.py         # Test client implementation
│   ├── server/            # Server implementation
│   │   ├── __init__.py
│   │   └── app.py        # Unified MCP server implementation
│   └── tools/             # Tool implementations
│       ├── __init__.py
│       └── echo.py       # Example tool implementation
├── pyproject.toml         # Project configuration
├── README.md             # Project documentation template
└── DEVELOPMENT.md        # Development guide template
```

## Next Steps

Once your project is generated:

1. Review and customize the README.md template
2. Follow DEVELOPMENT.md for:
   - Setting up the development environment
   - Installing dependencies
   - Running the server
   - Testing with the example client
   - Using MCP Inspector
3. Start adding your own tools in the `tools/` directory

## License

This template is licensed under the MIT License - see the LICENSE file for details.
