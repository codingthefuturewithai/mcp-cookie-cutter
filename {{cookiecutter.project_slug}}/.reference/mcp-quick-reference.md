# MCP Quick Reference

## For MCP Experts (Skip the Basics)

You know MCP. Here's what's unique about this implementation:

### What We Use
- **FastMCP** server with STDIO/SSE/Streamable HTTP transports
- **Tools** only (no resources, prompts, completions)
- **Context** for logging and progress
- **Type conversion** decorator handles string parameters

### Decorator Chain
```python
tool → type_converter → tool_logger → exception_handler → MCP
```

### Key Differences
1. **Automatic type conversion** from MCP's strings
2. **SQLite logging** of all executions
3. **Re-raise pattern** for error handling
4. **Preserved signatures** for introspection

### Quick Tool Pattern
```python
async def your_tool(param: str, count: int, ctx: Context = None) -> dict:
    """Your tool description."""
    # MCP sends strings, type_converter handles conversion
    return {"result": param * count}
```

## For Beginners (New to MCP)

### What is MCP?
Protocol that lets AI assistants (like Claude) use external tools to perform actions, not just generate text.

### Minimum to Know
1. **Tools = Python Functions** that AI can call
2. **Must be async** (`async def`)
3. **Need type hints** (`param: str`)
4. **Return JSON-compatible** data
5. **Parameters arrive as strings** (handled automatically)

### Your First Tool
```python
async def hello_world(name: str, ctx: Context = None) -> str:
    """Say hello to someone."""
    if ctx:
        ctx.info(f"Saying hello to {name}")
    return f"Hello, {name}!"
```

### Testing
```bash
# Start server
mcp dev your_project/server/app.py

# Open browser
http://localhost:6274

# Test your tool!
```

## Universal Truths (Both Levels)

### Cookie Cutter Structure
```
your_project/
├── server/app.py        # Main server (don't modify decorators)
├── tools/               # YOUR tools go here
├── decorators/          # Decorator system (don't modify)
└── tests/              # Integration tests
```

### Command Workflow
1. `/getting-started` - Understand the system
2. `/add-tool` - Create new tools
3. `/generate-tests` - Test your tools
4. `/dev-server` - Run and test
5. `/remove-examples` - Clean up for production

### What You Don't Need
- Resources (file serving)
- Prompts (templates)
- StreamableHTTP
- OAuth/Authentication
- WebSocket transport

## Version Note

This template tracks:
- **MCP Python SDK**: 1.0.0+
- **What we use**: ~20% of MCP features
- **What's stable**: Tool registration, Context, transports
- **What changes**: New features we don't use yet

## Need More?

- **Beginners**: Read `/mcp-beginners-guide.md`
- **Experts**: Read `/mcp-sdk-knowledge-base.md`
- **Everyone**: Check example tools in `tools/example_tools.py`