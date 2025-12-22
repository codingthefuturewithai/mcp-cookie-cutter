# MCP Version Tracker

This document tracks the relationship between MCP specification versions, Python SDK versions, and what this cookie cutter template actually implements.

## Current Versions (August 2025)

### MCP Specification
- **Latest Protocol Version**: `2025-06-18` (defined in spec)
- **Default Negotiated Version**: `2025-03-26` (when client doesn't specify)
- **Specification URL**: https://modelcontextprotocol.io/specification

### Python SDK
- **Package**: `mcp>=1.0.0`
- **GitHub**: https://github.com/modelcontextprotocol/python-sdk
- **PyPI**: https://pypi.org/project/mcp/

### Cookie Cutter Template
- **Template Version**: 1.0.0
- **Last SDK Sync**: August 2025
- **Implementation Level**: Basic (Tools + Context only)

## Feature Implementation Matrix

| Feature | SDK Support | Template Uses | Status |
|---------|------------|---------------|--------|
| **Core** | | | |
| Tools | ✅ Full | ✅ Yes | Stable |
| Context | ✅ Full | ✅ Partial | Stable |
| Type System | ✅ Full | ✅ Yes | Stable |
| **Transports** | | | |
| STDIO | ✅ Full | ✅ Yes | Stable |
| SSE | ✅ Full | ✅ Yes | Stable |
| WebSocket | ✅ Full | ❌ No | Available |
| StreamableHTTP | ✅ Full | ❌ No | New |
| **Advanced** | | | |
| Resources | ✅ Full | ❌ No | Stable |
| Prompts | ✅ Full | ❌ No | Stable |
| Completions | ✅ Full | ❌ No | Stable |
| Elicitation | ✅ Full | ❌ No | New |
| Sampling | ✅ Full | ❌ No | Experimental |
| OAuth/Auth | ✅ Full | ❌ No | New |
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
- `FastMCP()` - Constructor
- `server.tool()` - Tool registration
- `server.run_stdio_async()` - STDIO transport
- `server.run_sse_async()` - SSE transport

### Context Methods Used
- `ctx.info()`, `ctx.debug()`, `ctx.warning()`, `ctx.error()` - Logging
- `ctx.report_progress()` - Progress reporting

## Version Compatibility

### Minimum Requirements
- Python: 3.11+
- MCP SDK: 1.0.0+
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
- StreamableHTTP may become preferred transport
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
- StreamableHTTP (when stable)
- Authentication (for enterprise)