# MCP Server Cookie Cutter Template

This cookie cutter template helps you quickly scaffold a new MCP (Model Control Protocol) server project with a basic working implementation. The template includes a simple echo server with optional text transformation capabilities, demonstrating both required and optional parameters in MCP tools.

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- cookiecutter (`pip install cookiecutter`)

## Usage

### Option 1: Using the GitHub Repository

```bash
cookiecutter gh:codingthefuturewithai/mcp-cookie-cutter
```

### Option 2: Using Local Template

If you have the template locally:

```bash
cookiecutter path/to/mcp-cookie-cutter
```

## Template Configuration

During project creation, you'll be prompted for several values:

- `project_name`: The human-readable name of your project
- `project_slug`: The Python package name for your project (lowercase, no spaces)
- `server_port`: The port number for the SSE server (default: 8080)

## Project Structure

The generated project will have this structure:

```
your-project-name/
├── pyproject.toml           # Project dependencies and metadata
├── README.md               # Project documentation
└── your_project_name/      # Main package directory
    ├── __init__.py
    ├── server.py           # MCP server implementation
    └── client.py           # Example client implementation
```

## Getting Started with Your New MCP Server

1. Change into your new project directory:

   ```bash
   cd your-project-name
   ```

2. Create and activate a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install the project in development mode:

   ```bash
   pip install -e .
   ```

4. Test the server:

   ```bash
   # Terminal 1: Start the server
   your-project-name-server

   # Terminal 2: Run the client
   your-project-name-client "Hello, World!"

   # Try the optional case transformation
   your-project-name-client "Hello, World!" --transform upper
   your-project-name-client "Hello, World!" --transform lower
   ```

## Example Server Features

The template includes a simple echo server that demonstrates:

1. Basic MCP server setup
2. Tool registration with FastMCP
3. Required and optional parameters
4. SSE (Server-Sent Events) support
5. Logging configuration
6. Client implementation with Click CLI

### Echo Tool API

The server implements an echo tool with the following parameters:

- `text` (required): The text to echo back
- `transform` (optional): Case transformation option ('upper' or 'lower')

## Customizing Your Server

To add your own tools:

1. Open `server.py`
2. Add new tools in the `register_tools()` function using the `@mcp_server.tool` decorator
3. Update the client implementation in `client.py` as needed

Example of adding a new tool:

```python
@mcp_server.tool(
    name="your_tool",
    description="Description of your tool",
)
def your_tool(param1: str, param2: Optional[int] = None) -> str:
    """
    Your tool implementation

    Args:
        param1: Description of param1
        param2: Description of param2
    """
    # Your implementation here
    return result
```

## Development Best Practices

1. Always include descriptive docstrings for your tools
2. Implement proper error handling
3. Use type hints for parameters and return values
4. Add logging for important operations
5. Consider adding tests for your tools

## Contributing

If you find bugs or have suggestions for improving this template, please open an issue or submit a pull request on GitHub.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
