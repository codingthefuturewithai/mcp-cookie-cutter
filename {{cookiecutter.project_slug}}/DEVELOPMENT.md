# Developing Your MCP Server

This guide will help you get started with developing your own MCP server using the scaffolding provided.

## Initial Setup

1. Create and activate a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install the package in development mode:

   ```bash
   uv pip install -e .
   ```

3. Verify the scaffolding works by testing the included echo server:

   ```bash
   echo-with-transform-client "Hello, World"
   # Should output: Hello, World

   echo-with-transform-client "Hello, World" --transform upper
   # Should output: HELLO, WORLD
   ```

## Project Structure

The scaffolding provides a basic MCP server structure:

```
your-project/
├── server.py         # Main server implementation
├── pyproject.toml    # Package configuration and entry points
└── README.md        # Template for your server's documentation
```

Key files and their purposes:

- `server.py`: Contains the MCP server implementation and tool definitions
- `pyproject.toml`: Defines package metadata, dependencies, and command-line entry points

## Adding Your Own Tools

1. Open `server.py` and locate the tool registration section:

   ```python
   def register_tools(mcp_server: FastMCP) -> None:
       """Register all MCP tools with the server"""
   ```

2. Add your own tool using the `@mcp_server.tool` decorator:

   ```python
   from mcp import types

   @mcp_server.tool(
       name="your_tool_name",
       description="What your tool does"
   )
   def your_tool(param1: str, param2: int) -> types.TextContent:
       """
       Your tool's implementation.

       Args:
           param1: Description of param1
           param2: Description of param2

       Returns:
           TextContent: The result as MCP TextContent
       """
       result = process_your_data(param1, param2)

       return types.TextContent(
           type="text",
           text=result,
           format="text/plain"  # or "text/markdown", etc.
       )
   ```

### MCP Content Types

The MCP SDK defines the following content types for tool responses:

- `TextContent`: For text responses (plain text, markdown, etc.)
- `ImageContent`: For image data (PNG, JPEG, etc.)
- `JsonContent`: For structured JSON data
- `FileContent`: For file data with filename and MIME type
- `BinaryContent`: For raw binary data with optional MIME type

These types ensure:

- Proper type information in responses
- Consistent behavior across MCP implementations
- Better client compatibility
- Clear content format specification

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

3. Test your new tool:

   ```bash
   # Using stdio mode (default)
   your-mcp-server-client '{"tool": "your_tool_name", "arguments": {"param1": "value", "param2": 42}}'

   # Using the MCP Inspector
   mcp inspect your-mcp-server
   ```

## Transport Modes

Your MCP server supports two transport modes:

### stdio Mode (Default)

- Perfect for command-line tools and scripting
- No need to run a separate server process
- Automatically used by the client unless specified otherwise

### SSE Mode

- Ideal for web applications and long-running services
- Requires running the server explicitly:
  ```bash
  your-mcp-server --transport sse --port 3001
  ```
- Clients can connect via HTTP to `http://localhost:3001`

## Testing Your Server

1. Unit Tests

   - Add tests in the `tests/` directory
   - Test each tool's functionality
   - Test error cases and edge conditions

2. Integration Testing

   - Use the MCP Inspector for interactive testing:
     ```bash
     mcp inspect your-mcp-server
     ```
   - Test both stdio and SSE modes
   - Verify error handling and responses

3. Client Testing
   - Test with the command-line client
   - Test with Python client library
   - Test with web clients (for SSE mode)

## Documentation

1. Update the README.md template:

   - Replace all sections marked with [⚠️ CUSTOMIZE THIS SECTION]
   - Document your server's specific features
   - Update installation instructions if needed
   - Document your tools' API

2. Document your tools:
   - Clear descriptions
   - Parameter types and constraints
   - Return value specifications
   - Example usage

## Best Practices

1. Tool Implementation

   - Use type hints for all parameters
   - Provide clear docstrings
   - Handle errors gracefully
   - Return appropriate types

2. Error Handling

   - Use appropriate exception types
   - Provide helpful error messages
   - Handle both expected and unexpected errors

3. Configuration

   - Use environment variables for sensitive data
   - Provide clear configuration options
   - Document all settings

4. Testing
   - Write tests for all tools
   - Test error conditions
   - Test both transport modes
   - Verify type safety

## Next Steps

1. Remove the example echo tool once you have your own tools
2. Update package metadata in pyproject.toml
3. Add your own configuration options
4. Write comprehensive tests
5. Update documentation for your specific implementation

## Getting Help

- MCP Documentation: [Link to MCP docs]
- File issues on the repository
- Join the community [where applicable]

Remember: The echo server implementation is provided as a reference. Once you've implemented your own tools, you can remove it and update the documentation accordingly.
