# MCP Server Cookie Cutter Template

This template helps you create a new MCP (Model Control Protocol) server with minimal setup. MCP is a protocol that enables AI models to communicate with tools and services. This template provides a working example server that demonstrates MCP functionality through a simple echo service.

## What is MCP?

MCP (Model Control Protocol) is a protocol that allows AI models to:

- Call tools and functions
- Access resources
- Handle different types of content (text, files, etc.)
- Communicate over different transports (stdio, SSE)

The template creates a server that supports both stdio (standard input/output) and SSE (Server-Sent Events) communication.

## What is Cookie Cutter?

Cookie Cutter is a tool that creates projects from templates. Think of it like a project generator - you answer a few questions, and it creates a fully working project structure for you.

## Prerequisites

Before you start, you need:

1. Python 3.10 or higher installed

   ```bash
   python --version  # Should be 3.10 or higher
   ```

2. pip (Python package installer)

   ```bash
   pip --version  # Verify pip is installed
   ```

3. Cookie Cutter installed:
   ```bash
   pip install cookiecutter
   ```

## Creating Your MCP Server Project

1. Create a new project using this template:

   ```bash
   cookiecutter gh:codingthefuturewithai/mcp-cookie-cutter
   ```

2. You'll be asked several questions:

   - `project_name`: A human-readable name (e.g., "My Echo Server")
   - `project_slug`: Python package name (e.g., "my_echo_server")
   - `description`: Short description of your project
   - `author_name`: Your name
   - `author_email`: Your email
   - `server_port`: Port for SSE server (default: 3001)

3. This creates a new directory named after your project_slug containing a working MCP server.

## Setting Up Your New Project

1. Go to your new project directory:

   ```bash
   cd your-project-slug  # Replace with actual name
   ```

2. Create and activate a virtual environment:

   ```bash
   # On macOS/Linux:
   python -m venv venv
   source venv/bin/activate

   # On Windows:
   python -m venv venv
   venv\Scripts\activate
   ```

3. Install your project:
   ```bash
   pip install -e .
   ```

## Running Your MCP Server

Your project creates two server commands and a client:

1. Standard IO Server (default):

   ```bash
   your-project-slug-server
   ```

2. SSE Server (for MCP Inspector):

   ```bash
   # Default port (from cookie cutter config)
   your-project-slug-server-sse

   # Custom port
   your-project-slug-server-sse --port 4000
   ```

3. Test Client:
   ```bash
   your-project-slug-client "Hello, World!"
   your-project-slug-client "Hello, World!" --transform upper
   ```

## Testing with MCP Inspector

1. Start the SSE server:

   ```bash
   your-project-slug-server-sse  # Uses default port from config
   # OR
   your-project-slug-server-sse --port 4000  # Use custom port
   ```

2. Open MCP Inspector in your browser
3. Connect to `http://localhost:3001` (or your specified port)
4. Try the echo tool with different inputs

## Project Structure

```
your-project-slug/
├── pyproject.toml           # Project configuration and dependencies
├── README.md               # Project documentation
└── your_project_slug/      # Main package directory
    ├── __init__.py        # Package initialization
    ├── server.py          # Main server implementation
    ├── server_stdio.py    # Standard IO server entry point
    ├── server_sse.py      # SSE server entry point
    └── client.py          # Example client implementation
```

## Understanding the Code

- `server.py`: Main server logic and tool definitions
- `server_stdio.py`: Entry point for stdio mode (terminal usage)
- `server_sse.py`: Entry point for SSE mode (MCP Inspector)
- `client.py`: Example client showing how to use the server

## Echo Tool API

The template includes an echo tool that:

- Takes text input
- Optionally transforms it (upper/lower case)
- Returns the result

Parameters:

- `text` (required): Text to echo back
- `transform` (optional): Case transformation ('upper' or 'lower')

## Next Steps

1. Try the example commands above to verify everything works
2. Look at server.py to see how tools are defined
3. Add your own tools following the echo example
4. Update the README.md in your project with your specific details

## Getting Help

If you encounter issues:

1. Check the logs (the server prints debug information)
2. Ensure you're using the correct Python version
3. Verify all dependencies are installed
4. Open an issue on GitHub if you need help

## License

This template is licensed under the MIT License - see the LICENSE file for details.
