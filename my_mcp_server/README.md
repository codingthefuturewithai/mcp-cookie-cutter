# My MCP Server

MCP server with decorators

**[➡️ REPLACE: Expand on the description above. What problems does it solve? What capabilities does it provide to AI tools?]**

## Quick Start for MCP Clients

### 1. Install the MCP server (Recommended)

For the most reliable setup, first install the server as an isolated tool:

```bash
# Install the MCP server
uv tool install my_mcp_server

# Find the installed binary path
which my_mcp_server-server  # macOS/Linux
where my_mcp_server-server  # Windows
```

### 2. Configure your MCP client

Add this configuration to your MCP client settings using the absolute path from step 1:

**For Claude Desktop**: Add to `~/Library/Application Support/Claude/claude_desktop_config.json` (macOS) or `%APPDATA%\Claude\claude_desktop_config.json` (Windows)

**For Cline**: Add to `.vscode/settings.json` in your project

```json
{
  "my_mcp_server": {
    "command": "/absolute/path/to/my_mcp_server-server"
  }
}
```

**[➡️ REPLACE: If your server requires environment variables, show them here:]
```json
{
  "my_mcp_server": {
    "command": "/absolute/path/to/my_mcp_server-server",
    "env": {
      "API_KEY": "your-api-key-here",
      "BASE_URL": "https://api.example.com"
    }
  }
}
```
**[End of optional environment variables section]**

**Alternative: Quick start with uvx** (may have dependency conflicts):
```json
{
  "my_mcp_server": {
    "command": "uvx",
    "args": ["my_mcp_server-server"]
  }
}
```

### 3. Get your credentials (if needed)

**[➡️ REPLACE: If your server requires API keys or credentials, explain how to obtain them:]
- **API Key**: Get from https://example.com/api-keys
- **Base URL**: Your instance URL (e.g., https://api.example.com)
**[End of optional credentials section]**

### 4. Start using the tools

Once configured, you can ask your AI assistant to:
**[➡️ REPLACE: Add 2-3 example requests users might make:]
- "Use the echo tool to test the connection"
- "Transform 'hello world' to uppercase"

## Features

**[➡️ REPLACE: List the key features of your MCP server:]
- Example echo tool with text transformation
- Support for both stdio and SSE transports
- Comprehensive logging with automatic rotation
- Cross-platform compatibility (Linux, macOS, Windows)

## Available Tools

**[➡️ REPLACE: Document each tool your server provides. Follow this format for each tool:]

### echo

A simple tool for testing that echoes back the input text with optional transformations.

**Parameters:**
- `text` (required, string): The text to echo back
- `transform` (optional, string): Transform to apply - either "upper" or "lower"

**Returns:**
- JSON object containing:
  - `text`: The echoed text (possibly transformed)

**Examples:**

Basic echo:
```json
// Request
{
  "text": "Hello, World!"
}

// Response
{
  "text": "Hello, World!"
}
```

With transformation:
```json
// Request
{
  "text": "Hello, World!",
  "transform": "upper"
}

// Response
{
  "text": "HELLO, WORLD!"
}
```

## Alternative Configuration Methods

### Using a different MCP client

The configuration above works for Claude Desktop and Cline. For other MCP clients:

1. Use `uvx my_mcp_server-server` as the command
2. Set any required environment variables
3. Consult your MCP client's documentation for specific configuration format

### Using uv tool (Recommended for AI Assistants)

For isolated installation that avoids dependency conflicts:

```bash
# Install as an isolated tool
uv tool install my_mcp_server

# Find the installed binary location
uv tool list | grep my_mcp_server
# Or on macOS/Linux:
which my_mcp_server-server
# Or on Windows:
where my_mcp_server-server
```

Then use this configuration with the absolute path:
```json
{
  "my_mcp_server": {
    "command": "/path/to/my_mcp_server-server"
  }
}
```

**Note**: Replace `/path/to/` with the actual path from the commands above.

### Running from source

For development or testing from source code:

```json
{
  "my_mcp_server": {
    "command": "python",
    "args": ["-m", "my_mcp_server.server.app"],
    "env": {
      "PYTHONPATH": "/path/to/my_mcp_server"
    }
  }
}
```

## Installation Options

### Quick Start with uvx (Simplest)

The configuration above using `uvx` will automatically download and run the server without installation. This is the simplest option but may have conflicts if you have other Python packages installed globally.

### Isolated Installation with uv tool (Most Reliable)

For a clean, isolated installation that prevents dependency conflicts:

```bash
# Install the MCP server as an isolated tool
uv tool install my_mcp_server

# Verify installation and find the binary path
uv tool list | grep my_mcp_server

# Platform-specific path discovery:
# macOS/Linux:
which my_mcp_server-server
# Example output: /Users/username/.local/bin/my_mcp_server-server

# Windows:
where my_mcp_server-server
# Example output: C:\Users\username\.local\bin\my_mcp_server-server.exe
```

**Important**: After installation, update your MCP client configuration to use the absolute path returned by the `which` or `where` command.

### Install from Source (Development)

For development or testing from source code:

```bash
git clone <repository-url>
cd my_mcp_server

# Create and activate virtual environment
uv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
uv pip install -e .
```

Note: This requires the package to be published to PyPI. See [DEVELOPMENT.md](DEVELOPMENT.md#publishing-to-pypi) for publishing instructions.

## Troubleshooting

### Common Issues

**[➡️ REPLACE: Add common issues users might face. Here are some examples:]

1. **"Tool not found" error**
   - Ensure the server is running and properly configured
   - Check that the tool name is spelled correctly
   - Verify your MCP client is connected to the server

2. **Connection errors**
   - Check that no other process is using port 3001 (for SSE transport)
   - Verify your MCP client configuration is correct
   - Try restarting your MCP client

3. **Missing environment variables**
   - Ensure all required environment variables are set in your configuration
   - Check for typos in variable names
   - Verify credentials are valid and not expired

**[End of examples - customize based on your server's specific issues]**

### Dependency Conflicts

If you encounter dependency conflicts when using `uvx`:

1. **Use isolated installation instead**:
   ```bash
   # Install as an isolated tool to avoid conflicts
   uv tool install my_mcp_server
   
   # Find the binary path
   which my_mcp_server-server  # macOS/Linux
   where my_mcp_server-server  # Windows
   ```

2. **Update your MCP client configuration** to use the absolute path from step 1

3. **If conflicts persist**, check for conflicting global packages:
   ```bash
   # List all globally installed packages
   uv pip list
   
   # Consider using a virtual environment for development
   ```

## Requirements

- Python 3.11 or 3.12
- Operating Systems: Linux, macOS, Windows

**[➡️ REPLACE: Add any additional requirements specific to your MCP server:]
- Special system dependencies
- External services or APIs needed
- Network access requirements
- Hardware requirements (if any)
**[End of optional requirements]**

## Logging

The server logs all activity to both stderr and a rotating log file. Log files are stored in OS-specific locations:

- **macOS**: `~/Library/Logs/mcp-servers/my_mcp_server.log`
- **Linux**: `~/.local/state/mcp-servers/logs/my_mcp_server.log`
- **Windows**: `%LOCALAPPDATA%\mcp-servers\logs\my_mcp_server.log`

Logs rotate at 10MB with 5 backups kept. Control verbosity with `LOG_LEVEL`:

```bash
LOG_LEVEL=DEBUG uvx my_mcp_server-server
```

## Development

For development setup, testing, and contribution guidelines, see [DEVELOPMENT.md](DEVELOPMENT.md).

## AI Assistant Configuration

For detailed setup instructions for AI coding assistants (Claude, Cline, etc.), see [SETUP_PROMPT.md](SETUP_PROMPT.md).

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Author

tim - email@example.com

---

**[➡️ FINAL REMINDER: Replace all sections marked with ➡️ with content specific to your MCP server. Remove this reminder when done.]**