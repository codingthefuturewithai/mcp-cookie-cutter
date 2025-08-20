# MCP Compatibility - CRITICAL RULES

## ⚠️ MANDATORY: Never Use Optional Types in Parameters

**This is the #1 cause of MCP client failures!**

### ❌ NEVER DO THIS:
```python
from typing import Optional

async def my_tool(
    param1: Optional[str] = None,           # ❌ BREAKS MCP!
    param2: Optional[int] = None,           # ❌ BREAKS MCP!
    param3: Optional[List[str]] = None,     # ❌ BREAKS MCP!
    param4: Optional[Dict[str, Any]] = None # ❌ BREAKS MCP!
) -> str:
    ...
```

### ✅ ALWAYS DO THIS:
```python
async def my_tool(
    param1: str = "",                    # ✅ Empty string default
    param2: int = 0,                     # ✅ Zero default
    param3: List[str] = None,           # ✅ None default (becomes [])
    param4: Dict[str, Any] = None       # ✅ None default (becomes {})
) -> str:
    # Handle defaults in function body
    if param3 is None:
        param3 = []
    if param4 is None:
        param4 = {}
    ...
```

## Why This Matters

MCP clients (like Claude Desktop) send ALL parameters as strings over the wire. The type_converter decorator handles conversion, but Optional types cause the conversion to fail silently, resulting in:

- Parameters not being passed correctly
- Tools receiving None when they expect values
- Cryptic errors in MCP Inspector
- Silent failures in production

## The Rule Is Simple

**NEVER use Optional[...] in tool parameters. EVER.**

Use concrete types with sensible defaults instead:
- `str = ""` instead of `Optional[str]`
- `int = 0` or `int = -1` instead of `Optional[int]`
- `float = 0.0` instead of `Optional[float]`
- `bool = False` instead of `Optional[bool]`
- `List[...] = None` (handle in function) instead of `Optional[List[...]]`
- `Dict[...] = None` (handle in function) instead of `Optional[Dict[...]]`

## Testing for Compatibility

Before releasing any tool:

1. Check that NO Optional types exist in parameters
2. Test in MCP Inspector with missing parameters
3. Verify type conversion works correctly
4. Ensure defaults are handled properly

## Common Pitfalls

### Pitfall 1: IDE Auto-imports
Many IDEs automatically add `from typing import Optional` when you type `Optional`. Delete these imports immediately.

### Pitfall 2: Copy-Paste from Web
Most Python examples online use Optional. You MUST convert them to use concrete defaults for MCP.

### Pitfall 3: Assuming None Handling
Even if your function handles None correctly, the MCP transport layer may not. Always use concrete types.

## Remember

This is not a style preference. This is a HARD REQUIREMENT for MCP compatibility. Violating this rule WILL cause your tools to fail in production.