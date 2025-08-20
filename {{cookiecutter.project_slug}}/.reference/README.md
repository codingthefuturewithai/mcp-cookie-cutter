# MCP Reference Documentation

## ⚠️ DO NOT DELETE THIS DIRECTORY ⚠️

This `.reference/` directory contains permanent reference documentation and patterns that are used by AI assistants to help you develop MCP tools and tests. These references remain available even after you've removed all example code.

## Purpose

When you use commands like `/getting-started`, `/add-tool`, or `/generate-tests`, the AI assistant reads these reference documents first to ensure accurate, up-to-date information about MCP and consistent code generation.

## Contents

### Knowledge Base Documents

- **`mcp-quick-reference.md`** - Start here! Quick overview for all experience levels
- **`mcp-beginners-guide.md`** - Complete guide for those new to MCP
- **`mcp-integration.md`** - Advanced integration patterns for experts
- **`mcp-sdk-knowledge-base.md`** - What we use from the MCP SDK
- **`mcp-version-tracker.md`** - Version compatibility and updates

### `/patterns/` - Core Implementation Patterns

- **tool_patterns.py** - All MCP tool patterns with detailed explanations
- **integration_test_patterns.py** - MCP client integration test patterns  
- **unit_test_patterns.py** - Unit test patterns for decorators
- **decorator_patterns.py** - How decorators work and chain together

### `/templates/` - Code Generation Templates

- **new_tool_template.py.jinja** - Template for generating new tools
- **integration_test_template.py.jinja** - Template for integration tests
- **unit_test_template.py.jinja** - Template for unit tests

## How It Works

1. AI assistants ALWAYS read from `.reference/` first before generating code
2. Your actual code (which may diverge over time) is analyzed second
3. The AI combines reference patterns with your current code style

## Key Patterns Explained

### MCP Tool Pattern
```python
async def tool_name(param: type, ctx: Context = None) -> ReturnType:
    """Docstring explaining the tool."""
    # Implementation
    return result
```

### Integration Test Pattern
```python
async def test_tool_name():
    session, cleanup = await create_test_session()
    try:
        result = await session.call_tool("tool_name", arguments={...})
        assert result.isError is False  # or True for error cases
    finally:
        await cleanup()
```

### Decorator Application Order
- Regular tools: `@exception_handler → @tool_logger → tool`
- Parallel tools: `@exception_handler → @tool_logger → @parallelize → tool`

## Never Modify These Files

These reference patterns are carefully crafted to work with the decorator system and MCP protocol. Modifying them could cause AI assistants to generate incorrect code.