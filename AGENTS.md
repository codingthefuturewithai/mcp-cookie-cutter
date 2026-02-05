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

## MCP Design Principles (Applied in This Template)

These principles capture the lessons from the OneNote MCP refactor and align with this template’s
existing guidance and structure.

### Tool Schemas and Inputs
- Define explicit tool input schemas and canonical parameter names.
- Accept a minimal set of aliases only when you need backward compatibility.
- Validate inputs at the boundary and return actionable errors for missing/invalid params.

### Token Storage and Secrets
- Default to secure OS-backed storage where possible; provide file/env fallback.
- Make storage mode configurable and surface the effective mode in status/info.
- Avoid printing secrets in logs or commands; document safe setup paths.

### Pagination and Data Completeness
- Prefer pagination helpers for list endpoints to avoid partial results.
- Provide a consistent “fetch all pages” utility for list/read tools.

### Logging and Operational Clarity
- Emit structured logs to a file destination with optional console output.
- Add an `info`/status tool to expose version, config flags, and dependency checks.

### Versioning and Releases
- Use SemVer from package metadata and document tag-based release flow.
- Keep runtime version in server metadata and status tools.

### Testing Strategy
- Pair unit tests (parsers, helpers) with integration tests (mocked API/fetch).
- Make tests deterministic; avoid live network calls in CI.

### Documentation and Security Notes
- Provide `.env.example`, `LICENSE`, and security guidance for secrets handling.
- Document tool schemas, configuration, and known platform caveats.

### Standard Developer Workflow
- Use pre-commit hooks for lint/format/test in the generated project.
- Enforce commit message rules where possible (commitlint or equivalent).

### Language-Specific Guidance

If you are implementing the server in Python, follow the template’s default structure and
tooling (uv, pyproject, pytest, and the decorators/logging stack).

If you are implementing the server in Node/TypeScript, mirror the same principles with
TypeScript tooling: explicit schemas (zod or JSON schema), lint/format/test hooks, and a
build pipeline that emits runnable JavaScript.

### Template Guidance (Existing Structure)
- Keep tool logic isolated (`tools/`) and register via a single server entrypoint.
- Use absolute imports for clarity and stable packaging.
- Leverage decorators for error handling, logging, type conversion, and parallelism.