# Developing Your MCP Server

This guide will help you get started with developing your own MCP server using the scaffolding provided.

## Initial Setup

1. Create and activate a virtual environment:

   ```bash
   uv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install the package in development mode:

   ```bash
   uv pip install -e .
   ```

   **Note**: This step is REQUIRED before using `mcp dev` or running any server commands. Without it, you'll get `ModuleNotFoundError` when trying to import your package.

3. Verify the scaffolding works by testing the included echo server:

   ```bash
   # Test with stdio transport (default)
   {{ cookiecutter.project_slug }}-client "Hello, World"
   # Should output: Hello, World

   {{ cookiecutter.project_slug }}-client "Hello, World" --transform upper
   # Should output: HELLO, WORLD

   # Test with SSE transport
   {{ cookiecutter.project_slug }}-server --transport sse --port {{ cookiecutter.server_port }} &  # Start server in background
   # Wait a moment for the server to start, then:
   curl -s -N http://localhost:{{ cookiecutter.server_port }}/tools/echo -X POST -H "Content-Type: application/json" -d '{"text": "Hello SSE"}'
   # The output will be an SSE stream. Look for a data event like:
   # data: {"type":"text","text":"Hello SSE","format":"text/plain"}
   # Then, kill the background server job (e.g., 'kill %1' or 'fg' then Ctrl+C)
   ```

## Project Structure

The scaffolding provides a well-organized MCP server structure:

```
{{ cookiecutter.project_slug }}/              # Project Root
├── {{ cookiecutter.project_slug }}/          # Python package directory
│   ├── __init__.py      # Package initialization
│   ├── client/
│   │   ├── __init__.py  # Client module initialization
│   │   └── app.py       # Convenience client app for testing
│   ├── server/
│   │   ├── __init__.py  # Server module initialization
│   │   └── app.py       # Unified MCP server implementation
│   └── tools/
│       ├── __init__.py  # Tool module initialization
│       └── echo.py      # Example echo tool implementation
├── pyproject.toml       # Package configuration and entry points
├── README.md           # Project documentation
└── DEVELOPMENT.md      # Development guide (this file)
```

Key files and their purposes:

- `{{ cookiecutter.project_slug }}/{{ cookiecutter.project_slug }}/server/app.py`: Core MCP server implementation with unified transport handling and tool registration. This is the main server application module.
- `{{ cookiecutter.project_slug }}/{{ cookiecutter.project_slug }}/tools/`: Directory containing individual tool implementations (e.g., `echo.py`).
- `{{ cookiecutter.project_slug }}/{{ cookiecutter.project_slug }}/client/app.py`: Convenience client application for testing your MCP server.
- `pyproject.toml`: Defines package metadata, dependencies, and command-line entry points

## Adding Your Own Tools

1. Create a new file in the `tools/` directory for your tool:

   ```python
   # tools/your_tool.py
   from typing import Optional
   from mcp import types

   def your_tool(param1: str, param2: Optional[int] = None) -> types.TextContent:
       """Your tool implementation"""
       result = process_your_data(param1, param2)
       return types.TextContent(
           type="text",
           text=result,
           format="text/plain"
       )
   ```

2. Register your tool in `server/app.py`:

   ```python
   from {{ cookiecutter.project_slug }}.tools.your_tool import your_tool

   def register_tools(mcp_server: FastMCP) -> None:
       @mcp_server.tool(
           name="your_tool_name",
           description="What your tool does"
       )
       def your_tool_wrapper(param1: str, param2: Optional[int] = None) -> types.TextContent:
           """Wrapper around your tool implementation"""
           return your_tool(param1, param2)
   ```

### MCP Content Types

The MCP SDK defines the following content types for tool responses:

- `TextContent`: For text responses (plain text, markdown, etc.)
- `ImageContent`: For image data (PNG, JPEG, etc.)
- `JsonContent`: For structured JSON data
- `FileContent`: For file data with filename and MIME type
- `BinaryContent`: For raw binary data with optional MIME type

Examples using different content types:

```python
# Text response (e.g., for logs, markdown, etc.)
return types.TextContent(
    type="text",
    text="Your text here",
    format="text/plain"  # or "text/markdown"
)

# Image response
return types.ImageContent(
    type="image",
    data=image_bytes,
    format="image/png"  # or "image/jpeg", etc.
)

# JSON response
return types.JsonContent(
    type="json",
    data={"key": "value"}  # Any JSON-serializable data
)

# File response
return types.FileContent(
    type="file",
    data=file_bytes,
    format="application/pdf",  # MIME type
    filename="document.pdf"
)

# Binary response
return types.BinaryContent(
    type="binary",
    data=binary_data,
    format="application/octet-stream"  # Optional MIME type
)
```

## Testing Your MCP Server

The MCP Inspector provides a web-based interface for testing and debugging your MCP server during development.

### Starting the Inspector

**IMPORTANT**: You must install the package in development mode before using `mcp dev`:

```bash
# Step 1: Install the package in development mode (REQUIRED)
uv pip install -e .

# Step 2: Start the MCP Inspector pointing to your server module
# NOTE: You must set PYTHONPATH to the current directory for mcp dev to work
PYTHONPATH=. mcp dev {{ cookiecutter.project_slug }}/server/app.py
```

If you skip the installation step, you'll get a `ModuleNotFoundError` because Python won't be able to find your package imports.

This will:

1. Load your MCP server module
2. Start a development server
3. Launch the MCP Inspector web UI at http://localhost:5173

### Using the Inspector

In the MCP Inspector web interface:

1. Select the "Tools" tab to see all available tools
2. Choose a tool to test
3. Fill in the tool's parameters
4. Click "Run Tool" to execute
5. View the results in the response panel

The Inspector provides a convenient way to:

- Verify tool registration
- Test parameter validation
- Check response formatting
- Debug tool execution

### Example: Testing the Echo Tool

1. Select the "Tools" tab
2. Choose the "echo" tool
3. Parameters:
   - Enter text in the "text" field (e.g., "Hello, World!")
   - Optionally select a transform ("upper" or "lower")
4. Click "Run Tool"
5. Verify the response matches expectations

## Transport Modes

Your MCP server uses a single entry point, `{{ cookiecutter.project_slug }}-server`, and supports two transport modes, selectable via the `--transport` flag.

### stdio Mode (Default)

- **How it works**: The server communicates over standard input/output using JSON messages.
- **Use cases**: Ideal for command-line tools, scripting, and direct integration with other processes.
- **Invocation**: 
  - When you run `{{ cookiecutter.project_slug }}-client`, it automatically starts and communicates with `{{ cookiecutter.project_slug }}-server` in stdio mode.
  - To run the server directly in stdio mode (e.g., for testing with `mcp-cli` or other tools that manage the process):
    ```bash
    {{ cookiecutter.project_slug }}-server --transport stdio
    # Or simply, as stdio is the default:
    {{ cookiecutter.project_slug }}-server
    ```

### SSE (Server-Sent Events) Mode

- **How it works**: The server runs an HTTP server (using Uvicorn/Starlette) to handle MCP requests over Server-Sent Events.
- **Use cases**: Suitable for web-based clients, persistent connections, or when you need the server to be accessible over a network.
- **Invocation**:
  ```bash
  {{ cookiecutter.project_slug }}-server --transport sse --port {{ cookiecutter.server_port }}
  ```
  This starts the HTTP server, typically making it available at `http://localhost:{{ cookiecutter.server_port }}`. The MCP Inspector also connects to the server when it's running in this mode (or by pointing the Inspector directly to the `server/app.py` module).

## Deploying Your MCP Server

Once you've completed and tested your MCP server, you can make it available to AI coding assistants and other MCP clients:

1. Build a wheel distribution:

   ```bash
   python -m build --wheel
   ```

2. Install the wheel on your system:

   ```bash
   uv pip install dist/your_project-0.1.0-py3-none-any.whl
   ```

3. Locate the installed MCP server wrapper script:

   ```bash
   which your-mcp-server
   # Example output: /Users/username/.local/bin/your-mcp-server
   ```

4. Configure your AI coding assistant or other MCP clients to use this path when they need to access your MCP server's functionality.
