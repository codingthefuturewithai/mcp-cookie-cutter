# MCP SDK Knowledge Base

This document provides a comprehensive reference for the MCP (Model Context Protocol) SDK features that are actually used in this cookie cutter template. It is designed to be read by AI assistants to understand the current state of MCP as implemented in this template.

## Document Version
- **MCP Python SDK Version**: 1.0.0+ (as of August 2025)
- **Cookie Cutter Version**: MCP Server Cookie Cutter v1.0
- **Last Updated**: August 2025

## What This Cookie Cutter Uses from MCP

### Core MCP Components Used

1. **FastMCP Server** (`from mcp.server.fastmcp import FastMCP`)
   - High-level server interface
   - Triple transport support (STDIO, SSE, and Streamable HTTP)
   - Tool registration and management
   - Not using: Resources, Prompts, Completions

2. **Context Object** (`from mcp.server.fastmcp import Context`)
   - Provides access to MCP capabilities in tools
   - Logging to client (`ctx.info()`, `ctx.debug()`, etc.)
   - Progress reporting (`ctx.report_progress()`)
   - Not using: Resource reading, Elicitation

3. **MCP Types** (`from mcp import types`)
   - Tool definitions and schemas
   - Content blocks for responses
   - Error handling structures

4. **Transport Protocols**
   - **STDIO**: Standard input/output for CLI integration
   - **SSE**: Server-Sent Events for HTTP-based communication
   - **Streamable HTTP**: Modern unified HTTP transport with session management
   - Not using: WebSocket

### Features NOT Implemented in This Template

The following MCP features exist in the SDK but are NOT used in this cookie cutter:

1. **Resources**: File/data serving capabilities
2. **Prompts**: Prompt templates and management
3. **Completions**: Auto-completion support
4. **OAuth/Auth**: Authentication mechanisms
5. **WebSocket**: WebSocket transport (not implemented)
6. **Elicitation**: Interactive user input during tool execution
7. **Sampling**: LLM integration for message generation
8. **Roots**: File system access management

## How MCP Works in This Template

### 1. Server Initialization

```python
from mcp.server.fastmcp import FastMCP

# Create server with a name
server = FastMCP("My Server Name")
```

### 2. Tool Registration Pattern

Tools are registered using the `@server.tool()` decorator or `server.tool()` method:

```python
# Decorator approach (not used in template due to custom decorators)
@server.tool()
async def my_tool(param: str) -> str:
    return f"Result: {param}"

# Method approach (used in template)
server.tool(name="my_tool")(decorated_function)
```

### 3. Tool Function Requirements

All MCP tools MUST:
- Be async functions (`async def`)
- Have proper type hints for parameters
- Return JSON-serializable data (dict, list, str, int, float, bool)
- Optionally accept a `Context` parameter for MCP features

### 4. Parameter Handling

**Critical**: MCP passes ALL parameters as strings from the client. The template handles this with a `type_converter` decorator that automatically converts string parameters to the expected types based on function annotations.

```python
# MCP sends: {"n": "10"}  (string)
# Tool expects: n: int
# type_converter handles: "10" → 10
```

### 5. Error Handling

The template uses a re-raise pattern:
- Decorators catch exceptions
- Log the error
- Re-raise for MCP to handle
- MCP sets `isError = True` in response

## Transport Protocols

### STDIO Transport
- Used by: Claude Desktop, MCP Inspector, CLI tools
- Communication: JSON-RPC over standard input/output
- Configuration: Default transport mode

### SSE Transport
- Used by: Web applications, HTTP clients
- Communication: Server-Sent Events + POST endpoints
- Configuration: Requires port specification

### Streamable HTTP Transport
- Used by: Modern web applications, HTTP clients with session management
- Communication: Unified `/mcp` endpoint with POST/GET + SSE streaming
- Configuration: Requires port and endpoint specification
- Features: Session management, resumability, better performance

## Key Architectural Decisions

### Why These Features?

1. **Tools Only**: Most MCP servers primarily need tool functionality
2. **Triple Transport**: Covers CLI, traditional web, and modern web use cases
3. **Context for Logging**: Essential for debugging and user feedback
4. **No Resources/Prompts**: Complexity not needed for most use cases

### Decorator Integration Pattern

The template applies decorators in this order:
1. `type_converter` - Handles MCP's string parameters
2. `tool_logger` - Logs execution to SQLite
3. `exception_handler` - Catches and re-raises errors
4. `parallelize` (optional) - For batch operations

This preserves function signatures for MCP introspection while adding functionality.

## Common Pitfalls and Solutions

### 1. Parameter Type Mismatch
**Problem**: MCP sends strings, tools expect typed parameters
**Solution**: `type_converter` decorator handles conversion automatically

### 2. Synchronous Functions
**Problem**: MCP requires async functions
**Solution**: All tools must use `async def`

### 3. Non-JSON Return Values
**Problem**: Returning objects MCP can't serialize
**Solution**: Return only dict, list, str, int, float, bool

### 4. Missing Context Parameter
**Problem**: Tools that need Context but don't declare it
**Solution**: Add `ctx: Context = None` parameter

## Version Considerations

### What Changes Frequently
- Authentication mechanisms (OAuth support is new)
- Additional capabilities (Elicitation, Sampling are newer)
- Transport protocol improvements

### What Remains Stable
- Core tool registration and execution
- Transport protocols (STDIO, SSE, Streamable HTTP)
- Context object for logging
- JSON-RPC message format

## Testing Tools with MCP

### MCP Inspector
```bash
mcp dev path/to/server/app.py
```
- Interactive tool testing
- Parameter inspection
- Response validation

### Claude Desktop Integration
```json
{
  "mcpServers": {
    "my-server": {
      "command": "python",
      "args": ["-m", "my_server.server.app"]
    }
  }
}
```

## For AI Assistants

When helping users with this template:

1. **Assume**: Only tools, no resources/prompts
2. **Remember**: All parameters arrive as strings
3. **Enforce**: Async functions only
4. **Check**: Return types are JSON-serializable
5. **Consider**: Context parameter for logging

This knowledge base represents the ACTUAL MCP implementation in this template, not the full MCP specification. Focus on these features when assisting users.