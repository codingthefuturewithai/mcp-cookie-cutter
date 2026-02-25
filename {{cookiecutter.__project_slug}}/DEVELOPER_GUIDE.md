# Developer Guide - {{cookiecutter.project_name}}

This guide is for developers working on this MCP server - whether you're brand new to MCP or adding your tenth tool.

## 🚀 Quick Navigation

**Want a quick snapshot of this server?** Run `/server-overview` in Claude Code — it scans your project and tells you exactly what tools, deployment options, and configuration you have right now.

**First time with this server?** Start with [Step 1: Interactive Learning](#step-1-interactive-learning-first-time-developers)

**Returning to add features?** Jump to [Adding New Tools](#adding-new-tools-all-developers)

**Ready for production?** See [Preparing for Production](#preparing-for-production)

---

## Step 1: Interactive Learning (First-Time Developers)

If this is your first time working with this MCP server (or MCP in general), Claude Code provides an interactive tutorial:

```bash
# Start Claude Code in this directory
claude

# Run the interactive tutorial
/getting-started
```

This command will:

- Detect your experience level (new to MCP, new to this server, or experienced)
- Explain MCP concepts if needed
- Show you how THIS server's architecture works
- Demonstrate the decorator pattern
- Walk you through the example tools
- Test everything in MCP Inspector

**Time estimate**: 10-15 minutes for complete beginners, 5 minutes if you know MCP

---

## Step 2: Understanding This Server's Architecture

### What Makes This Server Special

This isn't a typical MCP server. It uses a **decorator pattern** which automatically adds:

- 🛡️ **Exception handling** - All errors are caught and returned cleanly
- 📊 **Logging** - Every tool execution is logged to SQLite
- 🔄 **Type conversion** - MCP sends strings, your tools get proper types
- ⚡ **Parallelization** - Process lists efficiently (optional)

### How Tools Are Registered

Unlike most MCP servers where you use `@mcp.tool` on each function, here:

1. You write a plain async function
2. Add it to a list (e.g., `my_tools = [func1, func2]`)
3. Import that list in `server/app.py`
4. The server automatically applies all decorators

**Why?** This ensures consistent error handling and logging across all tools.

---

## Adding New Tools (All Developers)

### Method 1: Claude Code Commands (Recommended)

Whether you're adding your first tool or your fiftieth:

```bash
# In Claude Code
/add-tool "description of what you want"

# Example:
/add-tool "fetch weather data for a given city"
```

This command will:

1. Research any needed libraries (uses context7 if available)
2. Create a detailed implementation plan
3. Wait for your approval
4. Generate the tool with proper typing
5. Register it in the server
6. Help you test it in MCP Inspector

### Method 2: Manual Tool Creation

If you prefer to write tools manually:

1. **Create your tool file**:

```python
# {{cookiecutter.__project_slug}}/tools/my_tools.py
from typing import Dict, Any
from fastmcp import Context

async def my_tool(
    param1: str,
    param2: int = 10,  # Use defaults, never Optional
    ctx: Context = None
) -> Dict[str, Any]:
    """Tool description for MCP."""
    # Your implementation
    return {"result": "data"}

# Export your tools
my_tools = [my_tool]  # Regular tools
my_parallel_tools = []  # Tools that process lists
```

2. **Register in server/app.py**:

```python
from {{cookiecutter.__project_slug}}.tools.my_tools import my_tools, my_parallel_tools
```

That's it! The decorators are applied automatically.

### Critical Rules for Tools

⚠️ **NEVER use Optional parameters** - they break MCP clients

```python
# ❌ WRONG
async def bad_tool(text: Optional[str] = None): ...

# ✅ CORRECT
async def good_tool(text: str = ""): ...
```

---

## Testing Your Tools

### Generating Tests Automatically

After creating a tool, generate comprehensive tests:

```bash
# In Claude Code
/generate-tests my_tool

# This creates:
# - Integration tests (MCP protocol testing)
# - Unit tests (if applicable)
# - Edge case tests
```

### Manual Testing with MCP Inspector

```bash
# Start the inspector
uv run mcp dev {{cookiecutter.__project_slug}}/server/app.py

# Opens at http://localhost:6274
# 1. Click "Connect" (left side)
# 2. Click "Tools" → "List Tools"
# 3. Find your tool and test it
```

### Running the Test Suite

After testing manually, run the automated test suite:

```bash
# Run all tests
uv run pytest

# Run only integration tests
uv run pytest tests/integration/

# Run with coverage report
uv run pytest --cov={{cookiecutter.__project_slug}} --cov-report=html

# Run specific test file
uv run pytest tests/integration/test_example_tools_integration.py -v
```

This is what CI/CD will run, so always verify tests pass before committing.

---

## Development Workflow Summary

### For New Developers

1. `/getting-started` - Learn the system
2. `/add-tool` - Create your first tool
3. `/generate-tests` - Generate tests
4. Test in MCP Inspector
5. `/remove-examples` - Clean up when ready

### For Returning Developers

1. `/add-tool` - Add new features
2. `/generate-tests` - Test them
3. Commit and push

---

## Preparing for Production

### Removing Example Code

Once you have your own tools working:

```bash
# In Claude Code
/remove-examples

# This removes:
# - All example tools
# - Example tests
# - References in server/app.py
```

### Deployment Checklist

- [ ] All example code removed
- [ ] Tests passing (`uv run pytest`)
- [ ] Configuration reviewed (`config.yaml`)
- [ ] README.md updated with your tools' documentation
- [ ] License and credits updated
- [ ] Docker deployment tested (`python scripts/docker.py start`)

---

## Project Structure Reference

```
{{cookiecutter.__project_slug}}/
├── server/
│   └── app.py           # Main server - imports and registers tools
├── tools/
│   └── example_tools.py # Example tools (remove when ready)
├── decorators/          # Decorators (don't modify)
├── tests/              # Test suite
├── scripts/
│   └── docker.py       # Docker management (start/stop/update)
├── Dockerfile          # Container build definition
├── docker-compose.yml  # Docker Compose configuration
├── .reference/         # Patterns and examples (always available)
└── .claude/commands/   # Claude Code commands
```

---

## Troubleshooting

### Import Errors

- Old MCP processes running → Kill them and restart
- Virtual environment issues → `uv sync`

### Tool Not Appearing

- Check it's in the export list (`my_tools = [...]`)
- Check it's imported in `server/app.py`
- Restart the MCP Inspector

### Tests Failing

- Check for Optional parameters (not allowed)
- Verify async function signature
- Ensure `ctx: Context = None` parameter exists

---

## Getting Help

1. **Reference examples**: Check `.reference/patterns/` for working code
2. **Claude Code**: Ask questions directly in your session
3. **Documentation**: See `docs/DECORATOR_PATTERNS.md` for deep technical details

---

## Next Steps

Ready to build? Start with:

```bash
claude
/getting-started  # If first time
# or
/add-tool "your tool idea"  # If returning
```

The commands will guide you through everything else!
