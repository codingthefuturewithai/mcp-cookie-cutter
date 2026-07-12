# MCP Version Tracker

This document tracks the relationship between MCP specification versions, Python SDK versions, and what this cookie cutter template actually implements.

## Current Versions (July 2026)

### MCP Specification
- **Latest Protocol Version**: `2025-06-18` (2026-07-28 spec in release-candidate stage)
- **Specification URL**: https://modelcontextprotocol.io/specification

### Python SDK
- **Package**: `mcp[cli]>=1.28.1,<2.0` (v2.x is a breaking rework for the 2026 spec - do not upgrade without migration)
- **GitHub**: https://github.com/modelcontextprotocol/python-sdk
- **PyPI**: https://pypi.org/project/mcp/

### Cookie Cutter Template
- **Template Version**: 1.1.0
- **Last SDK Sync**: July 2026 (SDK 1.28.1)
- **Implementation Level**: Tools + Structured Output + Annotations + Resources + Prompts + Elicitation

## Feature Implementation Matrix

| Feature | SDK Support | Template Uses | Status |
|---------|------------|---------------|--------|
| **Core** | | | |
| Tools | ✅ Full | ✅ Yes | Stable |
| Context | ✅ Full | ✅ Partial | Stable |
| Type System | ✅ Full | ✅ Yes | Stable |
| **Transports** | | | |
| STDIO | ✅ Full | ✅ Yes | Stable |
| Streamable HTTP | ✅ Full | ✅ Yes | Stable |
| WebSocket | ✅ Full | ❌ No | Available |
| **Advanced** | | | |
| Structured Output | ✅ Full | ✅ Yes | Stable |
| Tool Annotations/Titles | ✅ Full | ✅ Yes | Stable |
| Resources | ✅ Full | ✅ Yes | Stable |
| Prompts | ✅ Full | ✅ Yes | Stable |
| Stateless HTTP | ✅ Full | ✅ Optional (--stateless) | Stable |
| Completions | ✅ Full | ❌ No | Stable |
| Elicitation | ✅ Full | ✅ Yes | Stable |
| Sampling | ✅ Full | ❌ No | Stable |
| OAuth/Auth | ✅ Full | ❌ No | Stable |
| Roots | ✅ Full | ❌ No | Stable |

## What This Template Actually Uses

### From `mcp.server.fastmcp`
```python
from mcp.server.fastmcp import FastMCP  # Server class
from mcp.server.fastmcp import Context  # Context object
```

### From `mcp.types`
```python
from mcp import types  # Type definitions
```

### FastMCP Methods Used
- `FastMCP(name, instructions=..., transport_security=...)` - Constructor
- `server.tool(name=..., title=..., annotations=...)` - Tool registration with metadata
- `server.resource(uri, title=..., mime_type=...)` - Resource registration (incl. templates)
- `server.prompt(title=...)` - Prompt registration
- `server.run_stdio_async()` - STDIO transport
- `server.run_streamable_http_async()` - Streamable HTTP transport (settings: `stateless_http`, `json_response`)

### Context Methods Used
- `ctx.info()`, `ctx.debug()`, `ctx.warning()`, `ctx.error()` - Logging
- `ctx.report_progress()` - Progress reporting

## Version Compatibility

### Minimum Requirements
- Python: 3.11 - 3.14
- MCP SDK: 1.28.1+ (<2.0)
- UV: 0.5.0+ (package manager)

### Breaking Changes to Watch
1. **Parameter passing**: Currently strings, may change
2. **Error handling**: `isError` field format
3. **Transport protocols**: New ones added frequently
4. **Type specifications**: Evolving JSON Schema

## Update Strategy

### When to Update SDK
- **Security fixes**: Immediately
- **Bug fixes**: Next maintenance window
- **New features**: Only if needed
- **Breaking changes**: Major version only

### When to Update Template
- **SDK breaks compatibility**: Required
- **New stable features**: Optional
- **Community requests**: Evaluate
- **Security issues**: Immediately

## Migration Notes

### From Pre-1.0 SDK
- Import paths changed: `mcp.server.fastmcp` not `fastmcp`
- Context is now from `fastmcp` not `shared`
- Transport initialization changed

### Future Considerations
- Streamable HTTP is now the preferred HTTP transport
- OAuth may become required for some uses
- Resources/Prompts may be commonly needed
- Elicitation could be useful for interactive tools

## How to Check Versions

### Check Installed SDK Version
```bash
pip show mcp
uv pip show mcp
```

### Check Protocol Version in Code
```python
from mcp.types import LATEST_PROTOCOL_VERSION
print(LATEST_PROTOCOL_VERSION)  # e.g., "2025-06-18"
```

### Check Template Compatibility
```python
# In server/app.py
from mcp.server.fastmcp import FastMCP  # Should import without error
```

## Maintenance Checklist

When updating this template:

- [ ] Check latest MCP SDK version
- [ ] Review SDK changelog for breaking changes
- [ ] Test with new SDK version
- [ ] Update type_converter for parameter changes
- [ ] Verify MCP Inspector compatibility
- [ ] Test with Claude Desktop
- [ ] Update this version tracker
- [ ] Update knowledge base docs

## For AI Assistants

When helping users:

1. **Check user's SDK version first**
2. **Assume minimal feature set** (just tools)
3. **Don't recommend unimplemented features**
4. **Refer to this doc for capabilities**
5. **Test compatibility before suggesting updates**

## Version History

### July 2026
- Synced to MCP SDK 1.28.1 (pinned <2.0; v2 beta tracks the 2026 spec rework)
- Added structured output example (typed Pydantic tool return)
- Added tool titles + ToolAnnotations (readOnly/destructive/idempotent/openWorld hints)
- Added resources (static + template) and prompts examples
- Added --stateless / --json-response flags for Streamable HTTP
- Server now sends `instructions` at initialize
- Python range widened to 3.11-3.14

### August 2025
- Current stable release
- MCP SDK 1.0.0+ support
- Basic tool functionality
- Decorator integration fully tested

### Early 2025
- Initial template development
- MCP SDK integration begun
- Decorator pattern exploration

### Future (Planned)
- Resource support (if requested)
- Prompt templates (if needed)
- Additional transport options (if needed)
- Authentication (for enterprise)