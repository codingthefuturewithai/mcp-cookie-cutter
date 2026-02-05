# AGENTS.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this
repository.

## MCP Design Principles

These principles codify what worked well in a production MCP refactor and are intended to guide
new tools and changes.

### Tool Schemas and Inputs
- Define explicit input schemas with canonical parameter names.
- Use a small set of aliases only for compatibility, and normalize them early.
- Validate inputs at the boundary and return actionable errors.

### Token Storage and Secrets
- Prefer OS-backed secure storage with file/env fallback.
- Make storage mode configurable and visible via a status tool.
- Never print secrets in logs or command output.

### Pagination and Data Completeness
- Use pagination helpers for list and search endpoints.
- Provide consistent “fetch all” behavior in list/read tools.

### Logging and Operational Clarity
- Emit structured logs to a file destination with optional console output.
- Add an `info`/status tool for version, configuration, and dependency checks.

### Versioning and Releases
- Use SemVer sourced from package metadata.
- Document tag-based release flow and surface runtime version in server metadata.

### Testing Strategy
- Combine unit tests (helpers, schemas) with integration tests (mocked APIs/fetch).
- Keep tests deterministic and avoid real network dependencies.

### Documentation and Security Notes
- Ship `.env.example`, `LICENSE`, and security guidance for secret handling.
- Document tool schemas, configuration, and platform caveats.

### Standard Developer Workflow
- Use pre-commit hooks for lint/format/test checks.
- Enforce commit message rules where possible.

### Language-Specific Guidance

For Python servers, follow the default project structure and use Python-native tooling
(uv, pyproject, pytest, and the built-in decorators/logging stack).

For Node/TypeScript servers, apply the same principles with TypeScript tooling:
explicit schemas, lint/format/test hooks, and a build step that emits runnable JavaScript.
