# AGENTS.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 🚨 CRITICAL LEARNINGS - NEVER FORGET THESE

### Slash Commands CAN Pause and Wait for User Input

**PROVEN FACT:** Slash commands can absolutely pause mid-execution and wait for user responses. This works identically in both normal mode and plan mode.

**How:** Use the instruction `[WAIT FOR USER RESPONSE BEFORE CONTINUING]` in the slash command markdown. The agent will stop at that point, wait for user input, then continue with the same command context.

**Evidence:** The `/project:getting-started` command in generated projects pauses 20+ times during execution, asking questions and waiting for responses. This behavior is identical whether in plan mode or normal mode.

**Key Insights:**
- ✅ Slash commands ARE multi-turn capable
- ✅ Plan mode does NOT prevent slash commands from pausing
- ✅ Use `[WAIT FOR USER RESPONSE BEFORE CONTINUING]` to create interactive flows
- ✅ The slash command context persists across all these user interactions

**Example Pattern:**
```markdown
Present information here.

Do you understand?

[WAIT FOR USER RESPONSE BEFORE CONTINUING]

[If user says yes]:
- Continue to next concept

[If user says no]:
- Re-explain current concept
```

## Project Overview

This is a Python Cookiecutter template for creating MCP (Model Context Protocol) servers. MCP enables AI assistants to interact with external tools and services through a standardized protocol.

## Key Commands

### Template Development
```bash
# Create a new project from this template
cookiecutter .

# Install template dependencies (for development)
cd {{cookiecutter.__project_slug}}
uv pip install -e .
```

### Generated Project Commands
```bash
# Test with stdio transport (default)
{{cookiecutter.__project_slug}}-client "Hello, World"

# Test with SSE transport
{{cookiecutter.__project_slug}}-server --transport sse --port 3001

# Test with MCP Inspector
mcp dev {{cookiecutter.__project_slug}}/server/app.py

# Build distribution
python -m build --wheel
```

## Architecture

The template generates projects with this structure:
- `server/app.py`: Unified MCP server supporting both stdio and SSE transports
- `client/app.py`: Test client for development (stdio only)
- `tools/`: Directory for tool implementations (business logic)
- `config.py`: Runtime configuration management
- `logging_config.py`: OS-specific logging setup with file rotation

### Key Design Patterns

1. **Unified Transport Handling**: Single server codebase supports multiple transports via command-line arguments
2. **Tool Registration**: Tools are implemented separately and registered with the server
3. **Absolute Imports**: All imports use the full package path (e.g., `from {{cookiecutter.__project_slug}}.tools.echo import ...`)

### Adding New Tools

1. Create a new file in `tools/` directory
2. Implement tool functions following the pattern in `tools/echo.py`
3. Register the tool in `server/app.py` using `@mcp.tool()`

## Important Configuration

- Python 3.11-3.13 required
- Main dependencies: `mcp`, `anyio`, `starlette`, `uvicorn`
- Default SSE port: 3001 (configurable)
- Logging: Writes to OS-specific locations with 10MB rotation

## MCP-Specific Notes

- The server supports both stdio (for direct integration) and SSE (for HTTP-based access) transports
- Tools must handle various content types: Text, Image, JSON, File, Binary
- Use MCP Inspector for interactive development and testing
- The protocol requires proper error handling and response formatting

## MCP Design Principles

The template’s MCP design principles are consolidated in
`{{cookiecutter.__project_slug}}/docs/MCP_DESIGN_PRINCIPLES.md`. It covers:

- Tool schema conventions and canonical parameter names
- Token storage defaults, security guidance, and status reporting
- Pagination expectations for list/read tools
- Logging and operational status practices
- Versioning and release guidance
- Testing expectations (including mocked API responses)
- Language-specific guidance for Python vs Node/TypeScript

### Template Guidance (Existing Structure)
- Keep tool logic isolated (`tools/`) and register via a single server entrypoint.
- Use absolute imports for clarity and stable packaging.
- Leverage decorators for error handling, logging, type conversion, and parallelism.