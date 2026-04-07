---
description: Discover what this MCP server can do - tools, deployment options, and configuration
argument-hint: ""
allowed-tools: ["Read", "Grep", "Glob", "Bash"]
---

# Server Overview

Scan this project and present a comprehensive overview of what this MCP server can do right now.

## Instructions for AI Assistant

You are scanning the project to give the user a snapshot of their MCP server's current state. This is a read-only, single-pass summary — no modifications, no interactive pauses. Dynamically discover everything by reading actual source files.

### Step 1: Server Identity

1. Read `pyproject.toml` and extract:
   - `[project].name` — the package name
   - `[project].version`
   - `[project].description`
   - `[project.scripts]` — all entry points
2. Read `config.py` (find it via `Glob` for `**/config.py` excluding `__pycache__`) and extract:
   - `ServerConfig` defaults: name, description, default_transport, default_port, log_level

### Step 2: Discover Tools

1. Use `Glob` to find all `.py` files under the `tools/` directory (e.g., `**/tools/*.py`), excluding `__init__.py`
2. For **each** tool file found, `Read` it and extract:
   - Every `async def` function (these are the tools) — skip private functions starting with `_` and skip `get_tool_info` helper
   - The function's **docstring** (first line = description)
   - The function's **parameters** with types and defaults — skip `ctx: Context` (it's injected by the runtime)
   - Which **export list** the function belongs to (look for list assignments like `example_tools = [...]` or `parallel_example_tools = [...]` at the bottom of the file — the variable names tell you which are regular vs parallel)
3. Read `server/app.py` (find via `Glob` for `**/server/app.py`) and cross-reference:
   - Which tool lists are imported (e.g., `from ... import example_tools, parallel_example_tools`)
   - Confirm the tool registration loop — note the decorator chain applied to each category

### Step 3: Deployment Options

1. Check for Docker files:
   - `Glob` for `**/Dockerfile` and `**/docker-compose.yml`
   - `Glob` for `**/scripts/docker.py`
2. From `server/app.py` (already read), extract the CLI transport options from the `@click.option` for `--transport`
3. From `pyproject.toml` (already read), list all `[project.scripts]` entry points
4. Collect environment variables:
   - From `server/app.py`: look for `os.getenv()` calls (e.g., `MCP_DNS_REBINDING_PROTECTION`, `MCP_ALLOWED_HOSTS`)
   - From `config.py`: look for `os.getenv()` or `os.environ` calls
   - Common ones: `LOG_LEVEL`

### Step 4: Infrastructure

1. Check for `decorators/` directory via `Glob` for `**/decorators/*.py` (excluding `__init__.py`)
   - List each decorator file and its purpose (the filename tells you: `exception_handler`, `tool_logger`, `type_converter`, `parallelize`, `sqlite_logger`, etc.)
   - From `server/app.py`, identify the decorator chain order for regular tools vs parallel tools
2. Check for `ui/` directory via `Glob` for `**/ui/app.py`
   - If found, note the Streamlit admin dashboard is available
3. Check for `log_system/` directory via `Glob` for `**/log_system/*.py`
   - List logging destinations found under `**/log_system/destinations/*.py`
4. Read `logging_config.py` (find via `Glob`) for log file locations and rotation settings

### Presentation Format

Present your findings as a clean, scannable summary using this structure:

```
**[Server Name] v[version]**
[description from pyproject.toml]

---

**Tools ([total count]):**

_Regular tools ([count]):_
For each tool:
  - **tool_name** — [docstring first line]
    Parameters: param1 (type, required), param2 (type, default=X)

_Parallel tools ([count]):_
For each tool:
  - **tool_name** — [docstring first line]
    Parameters: param1 (type, required), param2 (type, default=X)

_Decorator chain:_
  - Regular: exception_handler → tool_logger → type_converter
  - Parallel: exception_handler → tool_logger → parallelize → type_converter

---

**Deployment:**
  - STDIO: `[entry-point-name]` or `python -m [package] --transport stdio`
  - Streamable HTTP: `[entry-point-name] --transport streamable-http --port [port]`
  - Docker: `python scripts/docker.py start` (if Dockerfile exists, otherwise omit)

**Entry points:**
  - List each from [project.scripts]

---

**Configuration:**
  - Config file: [path from config.py, e.g., platformdirs location]
  - Environment variables: LOG_LEVEL, MCP_DNS_REBINDING_PROTECTION, MCP_ALLOWED_HOSTS, etc.
  - Default transport: [value]
  - Default port: [value]

---

**Infrastructure:**
  - Logging: [destinations discovered] at [platform-specific paths from logging_config.py]
  - Admin UI: `streamlit run [package]/ui/app.py` (if ui/ exists, otherwise "Not installed")
  - Log system: [list destination types found, e.g., SQLite]
```

### Important Rules

- **Use Glob and Read tools** to discover everything dynamically — never hardcode tool names or assume what exists
- **Skip `__init__.py`** and `__pycache__` files when scanning directories
- **Skip `ctx: Context` parameter** when listing tool parameters (it's runtime-injected, not user-facing)
- **If tools/ is empty or has no tool functions**, say "No tools registered yet. Use `/add-tool` to create your first tool."
- **If a section has nothing to report** (e.g., no Docker files), omit it or note it briefly
- **Do NOT modify any files** — this is purely a read-only scan
- **Present everything in one pass** — no interactive pauses or questions
