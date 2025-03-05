# MCP Server Cookie Cutter Template

A cookie cutter template for creating new MCP (Model Control Protocol) servers. This template generates a fully functional MCP server with both stdio and SSE support, demonstrated through a simple echo service.

## Prerequisites

1. Python 3.10 or higher

   ```bash
   python --version  # Should be 3.10 or higher
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

- `project_name`: Human-readable name (e.g., "My Echo Server")
- `project_slug`: Python package name (e.g., "my_echo_server")
- `description`: Short description of your project
- `author_name`: Your name
- `author_email`: Your email
- `server_port`: Port for SSE server (default: 3001)

Once generated, follow the instructions in your new project's README.md for:

- Setting up the development environment
- Installing dependencies
- Running the server
- Testing with the example client
- Using the MCP Inspector

## License

This template is licensed under the MIT License - see the LICENSE file for details.
