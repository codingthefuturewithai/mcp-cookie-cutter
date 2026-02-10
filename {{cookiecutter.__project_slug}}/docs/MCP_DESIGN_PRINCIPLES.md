# MCP Design Principles

This document captures the MCP design principles used in this template so teams can align on
implementation and review expectations.

## Tool Schemas and Inputs
- Define explicit input schemas and canonical parameter names.
- Normalize aliases only when required for compatibility.
- Validate inputs at the boundary and return actionable errors.

## Token Storage and Secrets
- Prefer OS-backed secure storage with file/env fallback.
- Make storage mode configurable and visible through a status tool.
- Avoid logging or printing secrets in any output.

## Pagination and Data Completeness
- Use pagination helpers for list/search endpoints.
- Ensure list tools return complete results by default.

## Logging and Operational Clarity
- Emit structured logs to file with optional console output.
- Provide an `info`/status tool for version, config flags, and dependency checks.

## Versioning and Releases
- Use SemVer from package metadata.
- Document release tagging and expose runtime version in server metadata.

## Testing Strategy
- Pair unit tests for helpers with integration tests using mocked APIs/fetch.
- Keep tests deterministic and avoid live network calls in CI.

## Documentation and Security Notes
- Ship `.env.example`, `LICENSE`, and security guidance for secret handling.
- Document tool schemas, configuration, and platform caveats.

## Standard Developer Workflow
- Use pre-commit hooks for lint/format/test checks.
- Enforce commit message rules where possible.

## Language-Specific Guidance

For Python servers, use the template’s default structure and Python-native tooling
(uv, pyproject, pytest, and the decorators/logging stack).

For Node/TypeScript servers, apply the same principles with TypeScript tooling:
explicit schemas, lint/format/test hooks, and a build step that emits runnable JavaScript.
