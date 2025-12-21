# Feature Issue Example (Executable Spec)

This example shows the **structure and pattern** for Executable Spec issues.

**🎯 HOW TO USE THIS EXAMPLE:**

This example is from a **template/scaffolding project**. Your issue might be for:
- Web API (REST, GraphQL), microservice
- CLI tool, desktop app, mobile app
- Library, framework, infrastructure
- Database schema, DevOps automation

**Adapt the pattern** - don't copy verbatim. Focus on:
✅ **Outcome-focused acceptance criteria** (what the system can do)
✅ **Suggestive technical guidance** (recommend approaches, don't dictate code)
✅ **Generic enough to transfer** across project types

---

## Example: Project Template Generator

**Background & Goal:**

Development teams need a way to quickly scaffold new projects with consistent structure and best practices. Currently, setting up a new project requires manual creation of dozens of configuration files, directory structures, and boilerplate code, leading to inconsistencies and setup errors.

**Goal:** Provide an automated template system that generates new projects with customizable configuration and consistent structure.

---

## Acceptance Criteria

### 1. **Template Generation**
Users can generate new projects from the template with customizable project metadata (name, description, author details, target versions).

### 2. **Project Scaffolding**
Generated projects include organized directory structure for source code, tests, configuration files, and automation scripts.

### 3. **Development Tooling**
Generated projects include dependency management configuration, code quality tools (linting, formatting), and testing framework setup.

### 4. **Documentation**
Generated projects include README with setup instructions, usage examples, and contribution guidelines.

### 5. **Customization Hooks**
Template supports pre/post-generation hooks for project-specific customization logic.

---

## Technical Guidance

**Template Engine:**
- Consider cookiecutter (Python standard), Yeoman (JavaScript), or cargo-generate (Rust) depending on ecosystem
- Template should support variable substitution and conditional content

**Project Configuration:**
- Use ecosystem-standard configuration format (pyproject.toml for Python, package.json for Node, Cargo.toml for Rust)
- Follow PEP 517/518 for Python, use semantic versioning

**Code Quality:**
- Include configuration for ecosystem-standard linters and formatters
- Consider pre-commit hooks for automated quality checks
- Provide .gitignore for target ecosystem

**Cross-Platform:**
- Ensure generated paths work on Windows, macOS, and Linux
- Use forward slashes in templates for path compatibility

---

## Testing Requirements

- Verify template generates successfully with various input configurations
- Test variable substitution works correctly in all template files
- Validate generated project structure matches expected layout
- Test that generated project's tooling (tests, linters) works out of the box
- Verify hooks execute correctly during generation

---

## Key Characteristics

**Acceptance Criteria (5 items):**
- ✅ **Outcome-focused**: "Users can generate...", "Projects include...", "Template supports..."
- ✅ **Testable**: Each can be verified by attempting the described action
- ❌ **NOT implementation**: Doesn't say "Create file X" or "Use function Y"

**Technical Guidance:**
- ✅ **Suggestive**: "Consider cookiecutter", "Use ecosystem-standard format"
- ✅ **Rationale**: Explains WHY (Python standard, cross-platform, etc.)
- ❌ **NOT prescriptive**: Doesn't say "Call cookiecutter.main() in setup.py"

**Generic Transferability:**
- This pattern works for Python, JavaScript, Rust, Go templates
- AC describes capabilities, not Python-specific files
- Tech guidance adapts to ecosystem (pyproject.toml → package.json → Cargo.toml)
