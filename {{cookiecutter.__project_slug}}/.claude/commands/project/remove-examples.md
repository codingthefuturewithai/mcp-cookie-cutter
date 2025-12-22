---
description: Remove all example tools and tests after you've created your own - clean slate for production
argument-hint: ""
allowed-tools: ["Read", "Edit", "Glob", "Bash", "LS"]
---

# Remove Example Tools for Production

## 🚨 CRITICAL WARNING 🚨

**THE REGISTRATION LOOPS IN {{cookiecutter.__project_slug}}/server/app.py ARE SACRED - DO NOT TOUCH THEM!**

The ONLY thing you will modify in {{cookiecutter.__project_slug}}/server/app.py is the import statement. NOTHING ELSE.

## Prerequisites Check

**Before running this command, ensure:**
- ✅ You have created YOUR OWN tools
- ✅ YOUR tools are working in MCP Inspector  
- ✅ YOUR tests are passing (in your own test files)
- ⚠️ This is PERMANENT - no undo!

Let me verify you have your own tools first:

```bash
pwd
# List tools directory (cross-platform)
python -c "import os, pathlib; p = pathlib.Path('{{ cookiecutter.__project_slug }}/tools'); print([f.name for f in p.iterdir()] if p.exists() else 'Directory not found')"
```

Looking for YOUR tool files (not example_tools.py).

**STOP if no custom tools found!**

## Step 1: Remove Example Tool Files

```bash
# Remove the example tools module
# Windows:
del "{{ cookiecutter.__project_slug }}\tools\example_tools.py"
# Mac/Linux:
rm {{ cookiecutter.__project_slug }}/tools/example_tools.py

# Remove example-specific test files
# Windows:
del "tests\integration\test_example_tools_integration.py"
del "tests\integration\test_example_tools_edge_cases.py"
# Mac/Linux:
rm tests/integration/test_example_tools_integration.py
rm tests/integration/test_example_tools_edge_cases.py
```

## Step 2: Update {{cookiecutter.__project_slug}}/server/app.py - IMPORTS ONLY!

### 🛑 CRITICAL: ONLY MODIFY THE IMPORT LINE - NOTHING ELSE! 🛑

**YOU WILL ONLY REMOVE THIS ONE LINE:**
```python
from {{ cookiecutter.__project_slug }}.tools.example_tools import example_tools, parallel_example_tools
```

**That's it. STOP. Do not touch ANYTHING else in app.py.**

### ⚠️ DO NOT TOUCH THE REGISTRATION LOOPS! ⚠️

The registration loops that look like this:
```python
# Register regular tools with decorators
for tool_func in example_tools:
    # ... decorator application ...

# Register parallel tools with decorators  
for tool_func in parallel_example_tools:
    # ... decorator application ...
```

**THESE LOOPS MUST REMAIN EXACTLY AS THEY ARE!**

They will simply iterate over empty lists when the imports are removed. This is BY DESIGN.

**If you change these loops, you will DESTROY the entire server architecture.**

### Why This Works

The genius of this architecture is that the registration loops are GENERIC. They work with ANY list of tools:
- When example_tools is imported → loops register example tools
- When example_tools is NOT imported → loops iterate over empty lists (no error!)
- When you add YOUR tools → loops register YOUR tools

**The loops NEVER change. Only the imports change.**

## Step 3: Verify Clean Removal

```bash
# 1. Check server still imports correctly (use double quotes for Windows)
python -c "from {{ cookiecutter.__project_slug }}.server.app import app; print('Server imports successfully')"

# 2. List remaining test files (cross-platform)
python -c "import os, pathlib; p = pathlib.Path('tests/integration'); print([f.name for f in p.iterdir() if f.suffix == '.py'])"

# 3. Run YOUR tests (should all pass)
uv run pytest tests/integration/test_*.py -v

# 4. Verify example_tools import is gone
# Windows:
findstr "example_tools" {{cookiecutter.__project_slug}}\server\app.py || echo No example_tools import found
# Mac/Linux:
grep "example_tools" {{cookiecutter.__project_slug}}/server/app.py || echo "No example_tools import found"
```

## ✅ Cleanup Complete!

Your project now contains:
- ✅ YOUR working tools only
- ✅ YOUR passing tests only
- ✅ Clean server without example clutter
- ✅ INTACT registration loops (untouched!)
- ✅ Reference patterns still in `.reference/`

### What We Removed:
- `tools/example_tools.py` - All 6 example tools
- `test_example_tools_integration.py` - Example integration tests
- `test_example_tools_edge_cases.py` - Example edge case tests
- ONE import line from `{{cookiecutter.__project_slug}}/server/app.py` - NOTHING ELSE

### What Remains UNTOUCHED:
- **ALL registration loops in app.py** - These are SACRED
- YOUR tools in `tools/` directory
- YOUR tests
- Test infrastructure
- UI (unchanged)
- `.reference/` directory

## 🚨 FINAL WARNING 🚨

If you modified ANYTHING in {{cookiecutter.__project_slug}}/server/app.py besides removing the import line, you have likely broken the entire server. The registration loops are the CORE of the architecture and must NEVER be modified.

Remember:
- **ONLY remove the import line**
- **NEVER touch the registration loops**
- **The loops work with ANY tool lists - including empty ones**

This architecture is elegant and fragile. Respect it.