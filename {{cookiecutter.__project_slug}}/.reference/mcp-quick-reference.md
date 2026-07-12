# MCP Quick Reference

## For MCP Experts (Skip the Basics)

You know MCP. Here's what's unique about this implementation:

### What We Use
- **FastMCP** server with STDIO/Streamable HTTP transports (plus
  `--stateless` / `--json-response` for serverless)
- **Tools** with titles, `ToolAnnotations`, and structured output
  (typed Pydantic returns -> outputSchema + structuredContent)
- **Resources** (static + templates) and **Prompts** (string + multi-message)
- **Context** for logging, progress, and elicitation
- **Type conversion** decorator as defense-in-depth (SDK's Pydantic layer
  handles standard coercion natively)

### Decorator Chain
```python
tool → type_converter → tool_logger → exception_handler → MCP
```

### Key Differences
1. **SQLite logging** of all executions with correlation IDs
2. **Re-raise pattern** for error handling
3. **Preserved signatures** for introspection
4. **Per-tool metadata** via TOOL_METADATA (title + annotations)
5. **Extra type conversion** beyond the SDK's own Pydantic coercion

### Quick Tool Pattern
```python
async def your_tool(param: str, count: int, ctx: Context = None) -> dict:
    """Your tool description."""
    # SDK validates/coerces arguments via Pydantic before this runs
    return {"result": param * count}

# Structured output variant: return a typed model and the SDK publishes
# an outputSchema and returns validated structuredContent
async def typed_tool(city: str, ctx: Context = None) -> WeatherReport:
    ...
```

## For Beginners (New to MCP)

### What is MCP?
Protocol that lets AI assistants (like Claude) use external tools to perform actions, not just generate text.

### Minimum to Know
1. **Tools = Python Functions** that AI can call
2. **Must be async** (`async def`)
3. **Need type hints** (`param: str`)
4. **Return JSON-compatible** data
5. **Arguments are validated** against your type hints automatically

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
├── tools/               # YOUR tools go here (+ TOOL_METADATA)
├── resources/           # YOUR resources (static + templates)
├── prompts/             # YOUR prompts (message templates)
├── decorators/          # Decorator system (don't modify)
└── tests/              # Integration tests
```

### Command Workflow
1. `/getting-started` - Understand the system
2. `/add-tool` - Create new tools
3. `/generate-tests` - Test your tools
4. `/dev-server` - Run and test
5. `/remove-examples` - Clean up for production

### Also Included (Beyond Tools)
- Resources - read-only data addressed by URI (`resources/`)
- Prompts - reusable message templates, surfaced as slash commands (`prompts/`)

### What You Don't Need (Not in Template)
- OAuth/Authentication
- Completions, Sampling

## Version Note

This template tracks:
- **MCP Python SDK**: 1.28.1+ (<2.0 - v2 is a breaking rework)
- **What we use**: tools (+ annotations + structured output), resources,
  prompts, elicitation, progress, stateless HTTP
- **What's stable**: All of the above
- **Not yet used**: completions, sampling, OAuth

## Need More?

- **Beginners**: Read `/mcp-beginners-guide.md`
- **Experts**: Read `/mcp-sdk-knowledge-base.md`
- **Everyone**: Check example tools in `tools/example_tools.py`