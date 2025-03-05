# {{ cookiecutter.project_name }}

{{ cookiecutter.description }}

## Overview

**[⚠️ CUSTOMIZE THIS SECTION: Replace with a description of your specific MCP server's purpose and capabilities]**

This is a simple MCP (Model Control Protocol) server that provides an echo service. It demonstrates the basic principles of MCP server implementation and can be used as a testing tool for MCP clients or as a simple echo service in your infrastructure.

## Features

**[⚠️ CUSTOMIZE THIS SECTION: Replace these features with your MCP server's specific capabilities]**

- Echo service that returns any text sent to it
- Support for both SSE and stdio communication modes
- Asynchronous operation
- Type-safe responses
- Included reference client for easy testing

## Installation

### Local Development Setup

1. Clone or navigate to your project directory:

   ```bash
   cd {{ cookiecutter.project_slug }}
   ```

2. (Recommended) Create and activate a virtual environment:

   ```bash
   # Optional but recommended
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install the package in development mode:

   ```bash
   # This will install the package in "editable" mode
   pip install -e .
   ```

4. Test the installation:

   First, start the server in one terminal:

   ```bash
   {{ cookiecutter.project_slug }}-server
   ```

   You should see log output indicating the server has started.

   Then, in a new terminal (with the virtual environment activated if you're using one):

   ```bash
   {{ cookiecutter.project_slug }}-client "Hello, World!"
   ```

   You should see "Hello, World!" echoed back.

   Try the case transformation options:

   ```bash
   {{ cookiecutter.project_slug }}-client "Hello, World!" --transform upper
   # Should output: HELLO, WORLD!
   {{ cookiecutter.project_slug }}-client "Hello, World!" --transform lower
   # Should output: hello, world!
   ```

### Building and Installing from Wheel

If you want to build a wheel for distribution or local installation:

1. Install build tools:

   ```bash
   pip install build
   ```

2. Build the wheel:

   ```bash
   python -m build
   ```

   This will create both a source distribution (.tar.gz) and a wheel (.whl) in the `dist/` directory.

3. Install the wheel:
   ```bash
   pip install dist/{{ cookiecutter.project_slug }}*.whl
   ```

### Alternative Installation Methods

#### From Source (without virtual environment)

```bash
# Install directly in your Python environment
pip install .
```

#### From PyPI (if published)

If you choose to publish your package to PyPI:

```bash
pip install {{ cookiecutter.project_slug }}
```

## Usage

### Using the Client

The client uses stdio to communicate with the server, so you don't need to start the server separately. Simply use the client:

```bash
# Basic usage (just the message)
{{ cookiecutter.project_slug }}-client "Hello, World!"

# With case transformation
{{ cookiecutter.project_slug }}-client "Hello, World!" --transform upper
{{ cookiecutter.project_slug }}-client "Hello, World!" --transform lower
```

Expected output examples:

```bash
$ {{ cookiecutter.project_slug }}-client "Hello, World!"
Hello, World!

$ {{ cookiecutter.project_slug }}-client "Hello, World!" --transform upper
HELLO, WORLD!

$ {{ cookiecutter.project_slug }}-client "Hello, World!" --transform lower
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
        command="{{ cookiecutter.project_slug }}-server",
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
   {{ cookiecutter.project_slug }}-client "Your message here"
   ```

2. The MCP Inspector tool for interactive testing and debugging:

   ```bash
   mcp inspect {{ cookiecutter.project_slug }}-server
   ```

3. The Python client library for programmatic access:

   ```python
   from mcp import ClientSession, StdioServerParameters
   from mcp.client.stdio import stdio_client

   async def echo_message(message: str) -> str:
       server_params = StdioServerParameters(
           command="{{ cookiecutter.project_slug }}-server",
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
{{ cookiecutter.project_slug }}-server --port PORT  # Run on a different port (default: {{ cookiecutter.server_port }})
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
   {{ cookiecutter.project_slug }}-server --port DIFFERENT_PORT
   ```

2. **Connection Issues**

   - Verify the server is running
   - Check if the port is accessible
   - Ensure no firewall restrictions

3. **Import Errors**
   - Verify installation: `pip list | grep {{ cookiecutter.project_slug }}`
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
