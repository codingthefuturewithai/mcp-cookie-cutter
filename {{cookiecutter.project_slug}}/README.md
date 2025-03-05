# {{ cookiecutter.project_name }}

{{ cookiecutter.description }}

## Overview

This is a foundational MCP (Model Control Protocol) server project that provides the basic structure and plumbing needed to build your own MCP server. It includes:

- A complete MCP server implementation structure
- Built-in support for both stdio and SSE (Server-Sent Events) transport modes
- A simple echo tool as a reference implementation
- All necessary configuration and entry points

The project is ready for you to:

- Add your own MCP tools and functionality
- Customize the server configuration
- Build upon the existing transport handling

## Features

**[⚠️ CUSTOMIZE THIS SECTION: Replace these features with your MCP server's specific capabilities]**

- Complete MCP server infrastructure
- Built-in transport handling (stdio and SSE)
- Asynchronous operation support
- Type-safe request/response handling
- Example echo tool implementation

## Installation

### Local Development Setup

1. Create and activate a virtual environment:

   ```bash
   # Optional but recommended
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install the package in development mode:

   ```bash
   # This will install the package in "editable" mode
   uv pip install -e .
   ```

3. Test the installation:

   The scaffolding includes a simple echo server for testing. Try it with the echo client:

   ```bash
   echo-with-transform-client "Hello, World"
   ```

   You should see "Hello, World!" echoed back.

   Try the case transformation options:

   ```bash
   echo-with-transform-client "Hello, World" --transform upper
   # Should output: HELLO, WORLD!
   echo-with-transform-client "Hello, World" --transform lower
   # Should output: hello, world
   ```

## Development

Now that you've verified the scaffolding works, you can start building your own MCP server...

### Building and Installing from Wheel

If you want to build a wheel for distribution or local installation:

1. Install build tools:

   ```bash
   uv pip install build
   ```

2. Build the wheel:

   ```bash
   python -m build
   ```

   This will create both a source distribution (.tar.gz) and a wheel (.whl) in the `dist/` directory.

3. Install the wheel:
   ```bash
   uv pip install dist/your-mcp-server*.whl
   ```

### Alternative Installation Methods

#### From Source (without virtual environment)

```bash
# Install directly in your Python environment
uv pip install .
```

#### From PyPI (if published)

If you choose to publish your package to PyPI:

```bash
uv pip install your-mcp-server
```

## Usage

### Using the Client

The client uses stdio to communicate with the server, so you don't need to start the server separately. Simply use the client:

```bash
# Basic usage (just the message)
your-mcp-server-client "Hello, World!"

# With case transformation
your-mcp-server-client "Hello, World!" --transform upper
your-mcp-server-client "Hello, World!" --transform lower
```

Expected output examples:

```bash
$ your-mcp-server-client "Hello, World!"
Hello, World!

$ your-mcp-server-client "Hello, World!" --transform upper
HELLO, WORLD!

$ your-mcp-server-client "Hello, World!" --transform lower
hello, world!
```

### Python Integration

Here's how to use the echo server in your Python code:

```python
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def echo_message(message: str, transform: Optional[str] = None) -> str:
    # Create server parameters for stdio connection
    server_params = StdioServerParameters(
        command="your-mcp-server",
        args=[],
        env=None
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            # Call the echo tool with optional transform
            arguments = {"text": message}
            if transform:
                arguments["transform"] = transform

            result = await session.call_tool("echo", arguments=arguments)
            return str(result)

# Usage
message = await echo_message("Hello from Python!")  # Basic usage
upper_message = await echo_message("Hello from Python!", transform="upper")  # With transform
```

## API Reference

**[⚠️ CUSTOMIZE THIS SECTION: Document your server's specific tools and their parameters]**

### Echo Tool

```python
Tool: echo
Description: Returns the input text exactly as provided
Parameters:
    - text (str): The text to echo back
Returns:
    str: The exact input text
```

### Testing and Development

For testing and development, we recommend using:

1. The included command-line client:

   ```bash
   your-mcp-server-client "Your message here"
   ```

2. The MCP Inspector tool for interactive testing and debugging:

   ```bash
   mcp inspect your-mcp-server
   ```

3. The Python client library for programmatic access:

   ```python
   from mcp import ClientSession, StdioServerParameters
   from mcp.client.stdio import stdio_client

   async def echo_message(message: str) -> str:
       server_params = StdioServerParameters(
           command="your-mcp-server",
           args=[],
           env=None
       )

       async with stdio_client(server_params) as (read, write):
           async with ClientSession(read, write) as session:
               await session.initialize()
               result = await session.call_tool("echo", arguments={"text": message})
               return str(result)
   ```

These tools provide type-safe, reliable ways to interact with the server without dealing with low-level protocol details.

## Configuration

**[⚠️ CUSTOMIZE THIS SECTION: Document your server's specific configuration options]**

The server can be configured using command-line options:

```bash
your-mcp-server --port PORT  # Run on a different port (default: {{ cookiecutter.server_port }})
```

The server uses the following defaults:

- Host: localhost
- Port: {{ cookiecutter.server_port }}
- Logging: DEBUG level to stderr

## Troubleshooting

### Common Issues

**[⚠️ CUSTOMIZE THIS SECTION: Add troubleshooting specific to your server's functionality]**

1. **Port Already in Use**

   ```bash
   your-mcp-server --port DIFFERENT_PORT
   ```

2. **Connection Issues**

   - Verify the server is running
   - Check if the port is accessible
   - Ensure no firewall restrictions

3. **Import Errors**
   - Verify installation: `uv pip list | grep your-mcp-server`
   - Check Python version compatibility

### Getting Help

**[⚠️ CUSTOMIZE THIS SECTION: Update with your support channels]**

- File issues on our GitHub repository
- Contact: {{ cookiecutter.author_email }}
- Check logs using stderr output

## Requirements

- Python 3.10 or later (< 3.13)
- Operating Systems: Linux, macOS, Windows
- Dependencies:
  - mcp>=1.0.0
  - anyio>=4.5
  - starlette>=0.36.0
  - uvicorn>=0.27.0

## Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Author

{{ cookiecutter.author_name }} <{{ cookiecutter.author_email }}>

---

_A simple, reliable MCP echo server for your testing and development needs._

**[⚠️ FINAL REMINDER: This README template provides a structure for documenting your MCP server. Replace all sections marked with [⚠️ CUSTOMIZE THIS SECTION] with information specific to your implementation. Remove this reminder when done.]**
