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
   test_mcp_server-client "Hello, World"
   # Should output: Hello, World

   test_mcp_server-client "Hello, World" --transform upper
   # Should output: HELLO, WORLD

   # Test with SSE transport
   test_mcp_server-server --transport sse --port 3001 &  # Start server in background
   # Wait a moment for the server to start, then:
   curl -s -N http://localhost:3001/tools/echo -X POST -H "Content-Type: application/json" -d '{"text": "Hello SSE"}'
   # The output will be an SSE stream. Look for a data event like:
   # data: {"type":"text","text":"Hello SSE","format":"text/plain"}
   
   # To stop the background server:
   kill %1  # Kills the most recent background job
   # Or bring it to foreground and stop: fg then press Ctrl+C
   ```

## Project Structure

The scaffolding provides a well-organized MCP server structure:

```
test_mcp_server/              # Project Root
├── test_mcp_server/          # Python package directory
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

- `test_mcp_server/test_mcp_server/server/app.py`: Core MCP server implementation with unified transport handling and tool registration. This is the main server application module.
- `test_mcp_server/test_mcp_server/tools/`: Directory containing individual tool implementations (e.g., `echo.py`).
- `test_mcp_server/test_mcp_server/client/app.py`: Convenience client application for testing your MCP server.
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
   from test_mcp_server.tools.your_tool import your_tool

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

The Python MCP SDK defines the following content types for tool responses:

- `TextContent`: For text responses (plain text, markdown, etc.)
- `ImageContent`: For image data (PNG, JPEG, etc.)
- `AudioContent`: For audio data
- `EmbeddedResource`: For embedded resources

These are the only four content types available in the Python MCP SDK.

Examples using different content types:

```python
# Text response
return types.TextContent(
    type="text",
    text="Your text here"
)

# Image response
return types.ImageContent(
    type="image",
    data=base64_encoded_image_string,  # Base64 encoded image
    mimeType="image/png"  # or "image/jpeg", etc.
)

# Audio response
return types.AudioContent(
    type="audio",
    data=base64_encoded_audio_string,  # Base64 encoded audio
    mimeType="audio/mp3"  # or other audio MIME types
)

# Embedded resource response
# Note: resource field requires either TextResourceContents or BlobResourceContents
# For text resources:
return types.EmbeddedResource(
    type="resource",
    resource=types.TextResourceContents(
        uri="file:///path/to/resource.txt",
        mimeType="text/plain",
        text="The actual text content"
    )
)

# For binary resources:
return types.EmbeddedResource(
    type="resource",
    resource=types.BlobResourceContents(
        uri="file:///path/to/resource.pdf",
        mimeType="application/pdf",
        blob="base64_encoded_data"
    )
)
```

## Testing Your MCP Server

The MCP Inspector provides a web-based interface for testing and debugging your MCP server during development.

### Starting the Inspector

**IMPORTANT**: You must install the package in development mode AND set PYTHONPATH before using `mcp dev`:

```bash
# Step 1: Install the package in development mode (REQUIRED)
uv pip install -e .

# Step 2: Start the MCP Inspector pointing to your server module
# CRITICAL: PYTHONPATH must be set for module imports to work correctly
PYTHONPATH=. mcp dev test_mcp_server/server/app.py
```

⚠️ **WARNING**: If you run `mcp dev` without setting `PYTHONPATH=.`, you'll get a `ModuleNotFoundError` because Python won't be able to find your package imports. The PYTHONPATH tells Python to look in the current directory for modules.

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

Your MCP server uses a single entry point, `test_mcp_server-server`, and supports two transport modes, selectable via the `--transport` flag.

### stdio Mode (Default)

- **How it works**: The server communicates over standard input/output using JSON messages.
- **Use cases**: Ideal for command-line tools, scripting, and direct integration with other processes.
- **Invocation**: 
  - When you run `test_mcp_server-client`, it automatically starts and communicates with `test_mcp_server-server` in stdio mode.
  - To run the server directly in stdio mode (e.g., for testing with `mcp-cli` or other tools that manage the process):
    ```bash
    test_mcp_server-server --transport stdio
    # Or simply, as stdio is the default:
    test_mcp_server-server
    ```

### SSE (Server-Sent Events) Mode

- **How it works**: The server runs an HTTP server (using Uvicorn/Starlette) to handle MCP requests over Server-Sent Events.
- **Use cases**: Suitable for web-based clients, persistent connections, or when you need the server to be accessible over a network.
- **Invocation**:
  ```bash
  test_mcp_server-server --transport sse --port 3001
  ```
  This starts the HTTP server, typically making it available at `http://localhost:3001`. The MCP Inspector also connects to the server when it's running in this mode (or by pointing the Inspector directly to the `server/app.py` module).

## Deploying Your MCP Server

Once you've completed and tested your MCP server, you can make it available to AI coding assistants and other MCP clients:

1. Build a wheel distribution:

   ```bash
   # First, install the build tool if you haven't already
   uv pip install build
   
   # Then build the wheel
   python -m build --wheel
   ```

2. Install the wheel on your system using isolated installation:

   ```bash
   # Install as an isolated tool (recommended)
   uv tool install dist/your_project-0.1.0-py3-none-any.whl
   
   # Or install in current environment (for development)
   uv pip install dist/your_project-0.1.0-py3-none-any.whl
   ```

3. Locate the installed MCP server wrapper script:

   ```bash
   which your-mcp-server
   # Example output: /Users/username/.local/bin/your-mcp-server
   ```

4. Configure your AI coding assistant or other MCP clients to use this path when they need to access your MCP server's functionality.

## Publishing to PyPI

Once your MCP server is ready for public use, you can publish it to PyPI to make it easily installable via `pip` or `uvx`.

### Prerequisites

1. Create a PyPI account at https://pypi.org/account/register/
2. Generate an API token at https://pypi.org/manage/account/token/
3. Install publishing tools:
   ```bash
   uv pip install build twine
   ```
4. (Optional) Configure `.pypirc` for easier uploads:
   ```bash
   # Create ~/.pypirc with your API token
   cat > ~/.pypirc << EOF
   [pypi]
   username = __token__
   password = pypi-YOUR-API-TOKEN-HERE
   
   [testpypi]
   username = __token__
   password = pypi-YOUR-TEST-API-TOKEN-HERE
   EOF
   
   # Secure the file
   chmod 600 ~/.pypirc
   ```

### Prepare for Publishing

1. Update version in `pyproject.toml`:
   ```toml
   version = "0.1.0"  # Increment as needed
   ```

2. Ensure your README.md is complete and accurate
3. Verify all metadata in `pyproject.toml` is correct
4. Test your package locally:
   ```bash
   # Build the package
   python -m build --wheel
   
   # Install and test the built wheel
   uv pip install dist/test_mcp_server-*.whl
   test_mcp_server-server --help
   ```

### Publishing Process

1. Clean previous builds:
   ```bash
   rm -rf dist/ build/ *.egg-info/
   ```

2. Build the distribution:
   ```bash
   python -m build --wheel
   ```

3. Check the package:
   ```bash
   twine check dist/*
   ```

4. Upload to TestPyPI first (optional but recommended):
   ```bash
   twine upload --repository testpypi dist/*
   
   # Test installation from TestPyPI
   uv pip install --index-url https://test.pypi.org/simple/ test_mcp_server
   ```

5. Upload to PyPI:
   ```bash
   twine upload dist/*
   ```

   You'll be prompted for:
   - Username: `__token__`
   - Password: Your PyPI API token

### After Publishing

1. Test installation:
   ```bash
   # Install from PyPI as isolated tool
   uv tool install test_mcp_server
   
   # Verify installation
   uv tool list | grep test_mcp_server
   
   # Find binary location
   which test_mcp_server-server  # macOS/Linux
   where test_mcp_server-server  # Windows
   
   # Test with uvx (as fallback)
   uvx test_mcp_server-server --help
   ```

2. Update your README to remove "(if published)" notes
3. Tag the release in git:
   ```bash
   git tag v0.1.0
   git push origin v0.1.0
   ```

### Best Practices

- Use semantic versioning (MAJOR.MINOR.PATCH)
- Test thoroughly before publishing
- Include a CHANGELOG.md to document changes
- Never delete released versions from PyPI
- Use TestPyPI for testing the publishing process

## Troubleshooting

### ModuleNotFoundError

The most common issue when developing MCP servers is encountering `ModuleNotFoundError`. This project has been carefully structured to avoid such issues, but they can still occur in certain scenarios:

**When using MCP Inspector:**
```bash
# ❌ Wrong - will cause ModuleNotFoundError
mcp dev test_mcp_server/server/app.py

# ✅ Correct - sets PYTHONPATH
PYTHONPATH=. mcp dev test_mcp_server/server/app.py
```

**Important notes about project structure:**
- This template uses absolute imports throughout (e.g., `from test_mcp_server.tools.echo import ...`)
- The project structure and `__init__.py` files are carefully configured to support proper module discovery
- **DO NOT** restructure the project foundation, change import patterns, or modify core `__init__.py` files without understanding the implications

**If you encounter ModuleNotFoundError:**
1. Ensure you've installed the package in development mode: `uv pip install -e .`
2. Verify you're in the project root directory (where `pyproject.toml` is located)
3. Check that your virtual environment is activated
4. For MCP Inspector, ensure you're using `PYTHONPATH=.` before the command
5. Avoid modifying the project's import structure or `__init__.py` files
