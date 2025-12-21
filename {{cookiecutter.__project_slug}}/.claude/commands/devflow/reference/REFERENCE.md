# JIRA Issue Standards Reference

This guide provides standards and best practices for creating consistent, high-quality JIRA issues that work across different project types (web apps, APIs, CLIs, MCP servers, mobile apps, etc.).

---

## 🎯 Core Principle: Outcomes vs Implementation

**The most critical distinction when writing JIRA issues:**

### ✅ FOCUS ON: Outcomes, Capabilities, Requirements
- **WHAT** the system should do
- **WHAT** data/config is needed
- **WHAT** behavior users will see
- **WHAT** the acceptance criteria are

### ❌ AVOID: Implementation Details, Code Structure
- **HOW** to implement it (which functions to call)
- **HOW** to structure the code (which classes to create)
- **HOW** to architect the solution (which design patterns)

### Examples of the Difference

**Configuration/Data Requirements (BE SPECIFIC):**
```markdown
✅ GOOD: "Create config.yaml with fields: api_key, timeout, max_retries"
✅ GOOD: "Support JSON and YAML output formats via --format flag"
✅ GOOD: "Return user data including: id, name, email, created_at"
```
**Why good:** These are requirements about WHAT the system needs, not HOW to code it.

**Feature Capabilities (OUTCOME-FOCUSED):**
```markdown
✅ GOOD: "Provide memory monitoring including total, available, used, and free memory"
❌ TOO PRESCRIPTIVE: "Use psutil.virtual_memory() to get total, available, used, free"

✅ GOOD: "Support user authentication with email and password"
❌ TOO PRESCRIPTIVE: "Use bcrypt.hashpw() with cost factor 12 to hash passwords"

✅ GOOD: "Handle file uploads up to 100MB with progress indication"
❌ TOO PRESCRIPTIVE: "Use multer middleware with dest='./uploads' and add progress event emitter"
```

**Technical Guidance (SUGGEST, DON'T DICTATE):**
```markdown
✅ GOOD: "Consider psutil library for cross-platform system monitoring"
✅ GOOD: "Recommend bcrypt for password hashing (industry standard)"
✅ GOOD: "Suggest FastAPI framework for REST API endpoints"

❌ TOO PRESCRIPTIVE: "Use FastAPI's @app.post decorator in routes.py"
❌ TOO PRESCRIPTIVE: "Call bcrypt.hashpw() in auth/password.py line 45"
```

**Why This Matters:**

1. **Trust the developer**: They know how to implement features
2. **Flexibility**: Multiple valid approaches may exist
3. **Transferability**: Works across projects and tech stacks
4. **Maintainability**: Requirements don't change when code structure changes

---

## Acceptance Criteria Guidelines

Based on ACT-222 example, good acceptance criteria should be:

### 1. Specific and Measurable

Each criterion should have concrete, testable outcomes. Be specific about REQUIREMENTS (what, data, behavior) not IMPLEMENTATION (how, which functions).

**Examples:**

✅ **Good**: "Support user search by email, username, or full name with case-insensitive matching"

❌ **Too vague**: "Add user search"

❌ **Too prescriptive**: "Use SQLAlchemy's ilike() method in models/user.py to search email, username, name fields"

---

✅ **Good**: "Provide configuration file (config.yaml) with fields: api_key, timeout (seconds), max_retries (integer)"

❌ **Too vague**: "Set up configuration file"

❌ **Too prescriptive**: "Use PyYAML's safe_load() to parse config.yaml in utils/config.py"

---

✅ **Good**: "CLI accepts --format flag with 'json' or 'yaml' values and formats output accordingly"

❌ **Too vague**: "Add output formatting"

❌ **Too prescriptive**: "Use click.option() decorator with type=click.Choice(['json','yaml']) in cli.py"

### 2. Hierarchical Structure

Use bold titles with detailed sub-bullets for clarity and scannability.

**Format:**
```markdown
1. **[Area/Component Name]**: [Brief description of requirement]
    * [Specific detail with file names, values, or commands]
    * [Another specific requirement]
    * [Configuration or implementation detail]
```

**Example:**
```markdown
1. **Configuration Setup**: Create necessary configuration files:
    * `config.yaml` with API settings (openai_api_key, confluence credentials)
    * `.env.example` template with required variables
    * Default values for optional settings (timeout=30, max_retries=3)
```

### 3. Include Specific Details (for Requirements, Not Implementation)

**Be specific about WHAT, not HOW:**

✅ **Configuration files and data** (these ARE requirements):
- Configuration file names: `config.yaml`, `.env`
- Configuration fields: "api_key, timeout (default: 30), max_workers (default: 4)"
- API endpoints: `POST /api/v1/users`, `GET /api/v1/search`
- CLI flags: `--verbose`, `--format=json`, `--output=<path>`
- Data structures returned: `{id, name, email, created_at, updated_at}`

❌ **Source code files and implementation** (developer decides):
- Don't specify: "Create `src/utils/config.py`"
- Don't specify: "Add method to `UserService` class"
- Don't specify: "Use `bcrypt.hashpw()` function"

**Examples:**

✅ **Good - Specific requirement**: "API returns user data as JSON with fields: id, username, email, role, last_login"

❌ **Too prescriptive**: "Create User model in models/user.py with SQLAlchemy columns for id, username, email, role, last_login"

### 4. 5-7 Criteria per Feature

**Comprehensive but focused:**
- **Too few (1-3)**: Likely missing important details, incomplete specification
- **Just right (5-7)**: Comprehensive coverage of all aspects
- **Too many (10+)**: Should probably be broken into multiple issues

**Coverage areas to consider:**
1. Core functionality/feature
2. Configuration/setup requirements
3. Integration points
4. Error handling
5. Testing requirements
6. Documentation needs
7. Performance/optimization

### 5. Make Them Testable

Each criterion should be verifiable. Ask: "How will we know this is done?"

**Testable examples:**
- ✅ "Returns 404 status code when user not found"
- ✅ "Processes 1000 records per second"
- ✅ "Config file validates on startup and shows clear error for missing required fields"

---

## Technical Guidance Standards

Technical guidance should SUGGEST approaches and provide context, not dictate implementation. The goal is to inform developers, not micromanage them.

### 1. Version Requirements

Specify minimum versions or version ranges:

**Examples:**
- "Python 3.11+ required"
- "Node.js >= 18.0.0"
- "PostgreSQL 13-15 compatible"

### 2. Standards to Follow

Reference industry standards and best practices:

**Examples:**
- "Follow PEP 8 for Python code style"
- "Adhere to REST API design principles"
- "Follow ES6+ JavaScript standards"
- "Use semantic versioning (semver)"

### 3. Library/Technology Suggestions (Not Directives)

**SUGGEST libraries and explain WHY, don't dictate HOW to use them:**

✅ **Good - Suggestive**:
- "Consider psutil library for cross-platform system monitoring"
- "Recommend bcrypt for password hashing (industry standard, configurable cost factor)"
- "Suggest pytest framework for testing (follows existing project patterns)"
- "Consider FastAPI for REST endpoints (async support, automatic OpenAPI docs)"

❌ **Too prescriptive - Dictating implementation**:
- "Use psutil.virtual_memory() to get memory stats"
- "Call bcrypt.hashpw() with cost factor 12"
- "Use @pytest.fixture decorator in conftest.py"
- "Implement with @app.post('/endpoint') in routes/api.py"

**When suggesting tools, include context**:
- **Why**: Industry standard, performance, security, maintainability
- **Trade-offs**: "FastAPI for performance vs Flask for simplicity"
- **Alternatives**: "Consider X or Y depending on use case"

### 4. Cross-Platform Considerations

When relevant, address platform compatibility:

**Examples:**
- "Ensure all paths use forward slashes for cross-platform compatibility"
- "Test on Windows, macOS, and Linux"
- "Use `pathlib.Path` instead of string concatenation for file paths"
- "Avoid shell-specific commands; use Python standard library when possible"

### 5. Type Hints and Code Quality

When applicable, specify quality standards:

**Examples:**
- "Include type hints for all public functions"
- "Maintain 80%+ test coverage"
- "All new code must pass mypy strict mode"
- "Use dataclasses for structured data"

### 6. Configuration/Template Files

List configuration or template files needed (these are requirements, not code):

**Examples:**
- "Provide `.env.example` template documenting all required environment variables"
- "Include `docker-compose.yml` for local development environment"
- "Update `README.md` with setup instructions for new features"

❌ **Avoid specifying source code organization:**
- Don't say: "Add new endpoints to `src/api/v1/routes.py`"
- Instead: "Follow existing project patterns for organizing API routes"

### 7. Integration and Pattern Guidance

Guide developers to follow existing patterns without dictating exact implementation:

✅ **Good - Pattern-oriented**:
- "Follow existing authentication patterns in the codebase"
- "Use same error handling approach as other API endpoints"
- "Maintain consistency with existing logging patterns"
- "Integrate with current configuration system"

❌ **Too prescriptive - Code-level directives**:
- "Integrate with existing AuthMiddleware class in middleware/auth.py"
- "Use the EventEmitter pattern in services/notification.py"
- "Add validation in validators/user_validator.py using pydantic"
- "Import from utils.logger and call logger.info() at each step"

---

## Testing Requirements Standards

Testing requirements should specify what needs to be tested and how.

### 1. Unit Tests

What needs unit test coverage:

**Examples:**
- "Test each configuration parsing function with valid and invalid inputs"
- "Test all edge cases for date range calculations (leap years, timezone boundaries, DST transitions)"
- "Verify error messages are clear and actionable"

### 2. Integration Tests

End-to-end scenarios:

**Examples:**
- "Test complete workflow from feature request submission to API response"
- "Verify authentication → authorization → data access flow"
- "Test file upload → processing → storage → retrieval pipeline"

### 3. Edge Cases

Important edge cases to cover:

**Examples:**
- "Test with empty input"
- "Test with maximum length values (255 chars for names)"
- "Test with special characters in user input (@, #, %, etc.)"
- "Test concurrent access to shared resources"
- "Test network failure scenarios and retries"

### 4. Regression Tests

Prevent old bugs from returning:

**Examples:**
- "Verify fix doesn't break existing user search functionality"
- "Ensure backwards compatibility with v1 API responses"
- "Test that previous pagination bug doesn't reoccur"

### 5. Performance Tests

When relevant, specify performance requirements:

**Examples:**
- "Verify response time < 200ms for 95th percentile"
- "Test with 10,000 concurrent users"
- "Ensure memory usage stays below 512MB under normal load"

---

## Bug Report Standards

For bug reports (see BUG-EXAMPLE.md for full example):

### Always Include:
1. **Problem Statement**: 1-2 sentence summary of the issue
2. **Environment**: OS, versions, installation method, relevant config
3. **Steps to Reproduce**: Numbered, specific steps with exact commands
4. **Current Behavior**: What actually happens (with error messages)
5. **Expected Behavior**: What should happen instead

### Include When Available:
1. **Reference**: Link to GitHub issue, support ticket, related docs
2. **Debug Information**: Stack traces, logs, diagnostic output (in code blocks)
3. **Workaround**: Temporary solution if one exists
4. **Root Cause Analysis**: Technical explanation of the problem (if known)
5. **Investigation Areas**: Components/areas to investigate (not exact code fixes)
6. **Potential Approaches**: Suggested directions, not prescriptive solutions

**About "Proposed Solution" in Bug Reports:**

✅ **Good - Identifying problem areas**:
- "Issue appears to be in configuration file parsing logic"
- "Problem likely related to Windows file path handling"
- "Authentication token validation may not handle edge cases"

❌ **Too prescriptive - Dictating exact fixes**:
- "Fix by changing line 45 in config.py from yaml.load() to yaml.safe_load()"
- "Add try/except block in auth/validate.py around line 23"
- "Replace os.path.join with pathlib.Path in utils/files.py"

**Why:** Let developers diagnose and fix. Your analysis helps narrow the problem, but they know best how to fix their codebase.

### Be Specific:
- Include exact error messages
- Show command output in code blocks
- Provide file paths and line numbers when known
- List exact versions of all relevant software

---

## Priority Guidelines

Use these guidelines for consistent priority assignment:

### High Priority
- **Blocks development**: Team cannot continue work without this
- **Security issues**: Vulnerabilities, data exposure, auth bypasses
- **Data loss**: Risk of losing user data or corrupting database
- **Critical bugs**: Application crashes, core functionality broken
- **Production outages**: Live system is down or severely degraded

### Medium Priority
- **New features**: Planned functionality additions
- **Non-critical bugs**: Issues that have workarounds
- **Performance improvements**: Optimization work
- **Technical debt**: Refactoring, code quality improvements
- **User experience**: UI/UX improvements that aren't blocking

### Low Priority
- **Nice-to-haves**: Features that would be nice but aren't essential
- **Documentation**: Updates to docs, comments, guides
- **Minor refactoring**: Code cleanup that doesn't fix bugs or add features
- **Cosmetic issues**: Visual polish, minor UI tweaks

---

## Labels Best Practices

Labels help categorize and filter issues. Use them consistently.

### Label Categories:

1. **Technologies** (lowercase, kebab-case):
   - `python`, `typescript`, `react`, `postgresql`
   - `fastapi`, `pytest`, `docker`

2. **Components** (lowercase, kebab-case):
   - `api`, `ui`, `database`, `cli`
   - `auth`, `search`, `notifications`

3. **Type of Work**:
   - `bug`, `feature`, `refactor`
   - `documentation`, `testing`

4. **Platform** (when relevant):
   - `windows`, `macos`, `linux`
   - `ios`, `android`, `web`

### Formatting Rules:
- **Lowercase**: `mcp-server` not `MCP Server`
- **Kebab-case**: `cookie-cutter` not `cookie_cutter` or `cookiecutter`
- **Specific**: `mcp-server` not just `server`
- **Consistent**: Use same labels across similar issues

### How Many Labels?
- **Minimum**: 2-3 labels (technology + component + type)
- **Maximum**: 6-7 labels (more gets unwieldy)
- **Sweet spot**: 3-5 labels that accurately categorize the issue

**Example label sets:**
- Feature: `python`, `api`, `authentication`, `feature`
- Bug: `typescript`, `ui`, `react`, `bug`, `windows`
- Refactor: `python`, `cli`, `refactor`, `testing`

---

## Issue Type Decision Tree

**Is something broken or not working correctly?**
→ **Bug**

**Are you adding new functionality or capabilities?**
→ **Executable Spec**

**Is this maintenance, cleanup, or improvement of existing code without adding features?**
→ Consider if this should be a separate issue type (discuss with team) or use **Executable Spec** with appropriate labels

---

## Quick Checklist

Before creating an issue, verify:

### For Features (Executable Spec):
- [ ] Background & Goal section explains the "why"
- [ ] 5-7 specific, measurable acceptance criteria
- [ ] Technical guidance includes versions, standards, specific tools
- [ ] Testing requirements cover unit tests and integration scenarios
- [ ] Suggested labels extracted from technologies/components
- [ ] Priority assigned based on guidelines

### For Bugs:
- [ ] Problem statement is clear and concise
- [ ] Environment details are comprehensive
- [ ] Steps to reproduce are specific and numbered
- [ ] Current vs Expected behavior are in separate sections
- [ ] Proposed solution (if known) includes file paths
- [ ] Testing requirements specify verification steps
- [ ] Priority reflects severity and impact

---

## Remember

These standards exist to ensure:
1. **Consistency**: Team members know what to expect
2. **Clarity**: No ambiguity about requirements
3. **Quality**: Issues are complete and actionable
4. **Efficiency**: Developers have all info needed to implement
5. **Traceability**: Clear history of what was requested and why

When in doubt, look at FEATURE-EXAMPLE.md or BUG-EXAMPLE.md for reference!
