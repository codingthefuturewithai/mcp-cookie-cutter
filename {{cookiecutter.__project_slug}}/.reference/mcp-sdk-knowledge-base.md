# MCP SDK Knowledge Base

This document provides a comprehensive reference for the MCP (Model Context Protocol) SDK features that are actually used in this cookie cutter template. It is designed to be read by AI assistants to understand the current state of MCP as implemented in this template.

## Document Version
- **MCP Python SDK Version**: 1.28.1+ (<2.0) (as of July 2026)
- **Cookie Cutter Version**: MCP Server Cookie Cutter v1.1
- **Last Updated**: July 2026

## What This Cookie Cutter Uses from MCP

### Core MCP Components Used

1. **FastMCP Server** (`from mcp.server.fastmcp import FastMCP`)
   - High-level server interface
   - Dual transport support (STDIO and Streamable HTTP, with optional
     stateless / JSON-response modes for serverless deployments)
   - Tool registration with titles and `ToolAnnotations`
   - Resource registration (static URIs and templates)
   - Prompt registration (string and multi-message)
   - Server `instructions` sent to clients at initialize
   - Not using: Completions, Sampling, OAuth

2. **Context Object** (`from mcp.server.fastmcp import Context`)
   - Provides access to MCP capabilities in tools
   - Logging to client (`ctx.info()`, `ctx.debug()`, etc.)
   - Progress reporting (`ctx.report_progress()`)
   - Elicitation (`ctx.elicit()` - interactive user input, see elicit_example)
   - Not using: Resource reading from within tools

3. **MCP Types** (`from mcp import types`)
   - Tool definitions and schemas
   - Content blocks for responses
   - Error handling structures

4. **Transport Protocols**
   - **STDIO**: Standard input/output for CLI integration
   - **Streamable HTTP**: Modern unified HTTP transport with session management
   - Not using: WebSocket

### Features Implemented in This Template

1. **Tools**: with titles, `ToolAnnotations` behavior hints, and structured
   output (typed Pydantic returns publish an `outputSchema` and return
   validated `structuredContent` - see `get_weather` in example_tools)
2. **Resources**: static URIs and parameterized templates (`resources/`)
3. **Prompts**: reusable message templates (`prompts/`)
4. **Elicitation**: interactive user input mid-tool (`ctx.elicit`)
5. **Progress + client logging**: via Context
6. **Stateless Streamable HTTP**: `--stateless` / `--json-response` flags

### Features NOT Implemented in This Template

The following MCP features exist in the SDK but are NOT used in this cookie cutter:

1. **Completions**: Auto-completion support for prompt/resource arguments
2. **OAuth/Auth**: Authentication mechanisms (resource-server token verification)
3. **Sampling**: Server-initiated LLM calls (`ctx.session.create_message`)
4. **Roots**: File system access management

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

Modern MCP clients send **typed JSON** matching the tool's published input
schema, and the SDK (1.10+) validates and coerces arguments with Pydantic
before the tool function is called - a string `"10"` sent for an `int`
parameter is coerced natively.

The template's `type_converter` decorator remains as **defense-in-depth**
for non-conformant clients and for conversions Pydantic's lenient mode does
not perform (e.g. `"yes"`/`"on"` booleans, bare string -> single-item list).
It passes correctly-typed values through untouched.

```python
# Conformant client sends: {"n": 10}          -> passed through
# Legacy client sends:     {"n": "10"}        -> SDK/Pydantic coerces to 10
# Odd client sends:        {"flag": "yes"}    -> type_converter handles it
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

### Streamable HTTP Transport
- Used by: Modern web applications, HTTP clients with session management
- Communication: Unified `/mcp` endpoint with POST/GET + SSE streaming
- Configuration: Requires port and endpoint specification
- Features: Session management, resumability, better performance

## Key Architectural Decisions

### Why These Features?

1. **All Three Primitives**: Tools for actions, resources for read-only
   context, prompts for user-triggered workflows
2. **Dual Transport**: Covers CLI and web use cases (plus stateless mode
   for serverless)
3. **Context for Logging**: Essential for debugging and user feedback
4. **Annotations Everywhere**: Behavior hints let hosts build safer
   permission UX (advisory only - never rely on them for security)

### Decorator Integration Pattern

The template applies decorators in this order:
1. `type_converter` - Handles MCP's string parameters
2. `tool_logger` - Logs execution to SQLite
3. `exception_handler` - Catches and re-raises errors
4. `parallelize` (optional) - For batch operations

This preserves function signatures for MCP introspection while adding functionality.

## Common Pitfalls and Solutions

### 1. Parameter Type Mismatch
**Problem**: A non-conformant client sends strings where the schema says int/bool
**Solution**: SDK-level Pydantic coercion handles most cases; the
`type_converter` decorator covers the rest

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
- Transport protocols (STDIO, Streamable HTTP)
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

1. **Assume**: Tools, resources, AND prompts are all available patterns
2. **Remember**: Clients send typed JSON; the SDK validates with Pydantic
3. **Enforce**: Async functions only (template convention)
4. **Check**: Return types are JSON-serializable; prefer typed Pydantic
   models for structured output
5. **Consider**: Context parameter for logging/progress/elicitation
6. **Add**: A TOOL_METADATA entry (title + annotations) for every new tool

This knowledge base represents the ACTUAL MCP implementation in this template, not the full MCP specification. Focus on these features when assisting users.