# MCP Compatibility - Parameter Type Rules

## Current Status (SDK 1.28+, July 2026)

**`Optional[...]` parameters work correctly with the modern MCP SDK.** This was
empirically verified against `mcp==1.28.1`:

- `Optional[str] = None` / `str | None = None` parameters produce a valid
  `anyOf: [{type}, {"type": "null"}]` JSON schema
- Calls with the parameter omitted, provided, or explicitly `null` all succeed
- The SDK validates and coerces arguments with Pydantic *before* the tool
  function is called — string inputs like `"10"` for an `int` parameter are
  coerced natively, without any custom decorator

The hard "NEVER use Optional" rule that previous versions of this document
stated was a workaround for early-2025 MCP clients that sent all parameters
as strings and mishandled `anyOf`/null schemas. Conformant modern clients
(Claude Code, Claude Desktop, Cursor, MCP Inspector) send typed JSON and
handle Optional schemas correctly.

## Template Convention (Recommended, Not Required)

This template's example tools still prefer **concrete defaults** over Optional:

```python
async def my_tool(
    param1: str = "",                    # instead of Optional[str] = None
    param2: int = 0,                     # instead of Optional[int] = None
    param3: list[str] = [],              # instead of Optional[list] = None
) -> dict:
    ...
```

Why keep the convention:

1. **Maximal client compatibility** — non-conformant or older MCP clients
   still exist; simple scalar schemas are the lowest common denominator
2. **Simpler schemas** — a plain `{"type": "string"}` is easier for a model
   to satisfy than an `anyOf` union
3. **No None-handling branches** — concrete defaults remove a class of
   `if x is None` boilerplate

When Optional is the honest signature (e.g. "not provided" differs in meaning
from an empty value — see `threshold: float | None` style filters), use it.
It works.

## Defense-in-Depth: type_converter

The template's `type_converter` decorator predates the SDK's Pydantic
validation and remains as defense-in-depth for non-conformant clients. It
passes correctly-typed values through untouched and additionally handles
conversions Pydantic's lenient mode does not (e.g. `"yes"`/`"on"` booleans,
bare string → single-item list).

## Testing for Compatibility

Before releasing a tool:

1. Test in MCP Inspector with parameters omitted, provided, and (for
   Optional) explicitly null
2. Verify the generated `inputSchema` in `tools/list` looks reasonable
3. If you target older/unknown clients, prefer concrete defaults

## History

- **Pre-2025-06 (this doc's original guidance):** several MCP clients sent
  all parameters as strings and failed on Optional/anyOf schemas — Optional
  was a genuine production hazard, hence the original hard rule
- **SDK 1.10+ / mid-2025 onward:** Pydantic-based argument validation and
  coercion made typed and Optional parameters reliable on conformant clients
- **July 2026 (this revision):** rule downgraded from hard requirement to
  convention, verified against mcp 1.28.1
