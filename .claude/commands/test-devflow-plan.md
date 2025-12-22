---
description: Test plan-work flow with real analysis on this repo
argument-hint: "[--tdd]"
allowed-tools: ["Grep", "Glob", "Read", "EnterPlanMode"]
---

# Test Plan Work Flow

I'll analyze a mock issue and develop a detailed implementation plan on THIS cookiecutter repo.

Issue: $ARGUMENTS (default: TEST-123)

[Call `EnterPlanMode`]

Now in Plan Mode - I'll fetch the issue details and analyze the codebase.

[Check if $ARGUMENTS contains --tdd flag]

**TDD Mode:** [If --tdd present: ENABLED | If absent: DISABLED]

[If --tdd mode enabled, notify user]:
✅ TDD Mode enabled - I will:
- Detect test framework and patterns
- Map existing tests to modified components
- Generate test cases from acceptance criteria
- Plan RED/GREEN/REFACTOR workflow for implementation

[If --tdd mode disabled]:
To enable Test-Driven Development workflow, use: `/test-devflow-plan --tdd`

---

## Step 1: Fetch Issue Details

**MOCK JIRA DATA (simulating real fetch):**

Issue: TEST-123 - Add validation helper for cookiecutter variables
Type: Feature

**Description:**
Add a Python helper function to validate cookiecutter.json variables before template generation. Should check:
- Required fields are present
- Email format is valid
- Project slug follows naming conventions
- Python version is supported

**Acceptance Criteria:**
1. Function validates all required fields in cookiecutter.json
2. Returns clear error messages for invalid data
3. Includes unit tests with 100% coverage
4. Documents validation rules in docstrings

---

## Step 2: Analyze Codebase & Create Implementation Plan

### Analyze Codebase

**Search for related code:**
[Use Glob to find Python files in this repo]
[Use Glob to find existing test files]
[Read key files to understand patterns]

**Findings:**
[Report actual files found - hooks/*, {{cookiecutter.__project_slug}}/*, etc.]
- Related files: [list actual Python files]
- Code patterns: [analyze actual import style, error handling from hooks/post_gen_project.py]
- Test patterns: [analyze if any tests exist]
- Integration points: [cookiecutter hooks, template validation]

### Test Strategy Analysis (if --tdd flag present)

[Only if TDD Mode is ENABLED]

**Test Framework Detection:**
[Search codebase to discover test infrastructure - adapt to what exists]

1. **Find test files:**
   [Glob for: tests/, test/, *test*.py, *_test.py]
   [Read pyproject.toml or setup.py if exists]

2. **Identify frameworks by analyzing what's found:**
   [If test files found: Read them to see imports (pytest, unittest, etc.)]
   [If no tests: Report "No existing test infrastructure found"]

3. **Report discovered test infrastructure:**
   - Languages detected: [Python - confirmed from .py files]
   - Frameworks found: [pytest/unittest/none - based on actual findings]
   - Test locations: [actual paths found or "none - need to create"]
   - Run commands: [pytest/python -m unittest/TBD]
   - Run specific: [pytest path/to/test_file.py::test_name]

If NO tests found: Note this and skip test mapping (still generate test plan for TDD)

**Existing Test Patterns:**
[If tests exist: Read 2-3 test files to extract patterns]
[If no tests: Skip this section]

**Relevant Existing Tests:**
[If tests exist: Try to map to cookiecutter validation logic]
[If no tests: "No existing tests - this will be first test suite"]

**New Tests Required:**
[Extract testable behaviors from acceptance criteria]

AC #1: "Function validates all required fields in cookiecutter.json"
Testable behaviors:
- Returns success when all required fields present
- Raises error when required field missing
- Identifies which field is missing in error message

Test cases needed:
- test_validate_all_fields_present_success()
- test_validate_missing_project_name_raises_error()
- test_validate_missing_email_raises_error()

AC #2: "Returns clear error messages for invalid data"
Testable behaviors:
- Email validation catches invalid formats
- Project slug validation catches invalid characters
- Error messages are human-readable

Test cases needed:
- test_invalid_email_format_error()
- test_invalid_project_slug_error()
- test_error_message_includes_field_name()

AC #3: "Includes unit tests with 100% coverage"
Testable behaviors:
- All code paths covered
- Edge cases tested

Test cases needed:
- test_empty_cookiecutter_json()
- test_none_value_in_required_field()

Test files to create:
- tests/unit/test_cookiecutter_validator.py
  (will establish pattern for this repo if no tests exist)

**TDD Implementation Order:**
Each logical unit follows: Write tests (RED) → Implement (GREEN) → Refactor → Validate

### Implementation Plan

**For Features:**
- Logical components to build
- Files to create/modify
- Code patterns to follow
- Test strategy
- Integration points

**Specific Plan for TEST-123:**

1. **Create validation module:**
   - File: hooks/cookiecutter_validator.py
   - Imports: json, re, pathlib
   - Functions: validate_config(), validate_email(), validate_slug()
   - Error handling: Custom ValidationError class

2. **Integration with hooks:**
   - Modify: hooks/pre_gen_project.py
   - Add: from cookiecutter_validator import validate_config
   - Call validation before template generation

3. **Test infrastructure:**
   [If no tests exist: Set up pytest infrastructure]
   - Create: tests/unit/ directory
   - Create: tests/conftest.py for fixtures
   - Create: tests/unit/test_cookiecutter_validator.py
   - Add pytest to dev dependencies

**All Plans Include:**

**Code Pattern Compliance:**
[Based on analysis of hooks/post_gen_project.py]:
- Follow discovered import patterns
- Follow error handling conventions
- Follow logging patterns
- Follow module structure
- Maintain modular design

**Documentation Updates:**
[Glob for *.md files in repo]
- Update README.md with validation feature
- Add docstrings to all functions
- Create docs/validation.md if complex

**Validation Strategy:**
- Features: Unit/integration tests following existing patterns
- Run pytest with coverage
- Manual test with sample cookiecutter.json

**Commit Strategy:**
- Commit after each logical unit is validated
- Reference issue key in commits

**Implementation Order:**

[If TDD Mode is DISABLED]:
1. Create cookiecutter_validator.py module
2. Write validation functions
3. Add tests
4. Integrate with hooks
5. Update documentation

[If TDD Mode is ENABLED]:

**TDD-Enhanced Implementation Order:**

1. Validation Module Setup
   - **RED**: Write tests in tests/unit/test_cookiecutter_validator.py
     - test_validate_all_fields_present_success()
     - test_validate_missing_project_name_raises_error()
     - test_validate_missing_email_raises_error()
   - **Run**: pytest tests/unit/test_cookiecutter_validator.py → EXPECT RED (tests fail)
   - **GREEN**: Implement hooks/cookiecutter_validator.py with validate_config()
   - **Run**: pytest tests/unit/test_cookiecutter_validator.py → EXPECT GREEN (tests pass)
   - **Validate**: pytest (all tests) → STAY GREEN
   - **Commit**: "feat: Add cookiecutter config validator with tests\n\nRefs: TEST-123"

2. Email Validation
   - **RED**: Write tests in tests/unit/test_cookiecutter_validator.py
     - test_valid_email_passes()
     - test_invalid_email_format_error()
   - **Run**: pytest tests/unit/test_cookiecutter_validator.py::test_invalid_email_format_error → EXPECT RED
   - **GREEN**: Implement validate_email() function
   - **Run**: pytest tests/unit/test_cookiecutter_validator.py → EXPECT GREEN
   - **Validate**: pytest → STAY GREEN
   - **Commit**: "feat: Add email validation with tests\n\nRefs: TEST-123"

3. Slug Validation
   - **RED**: Write tests for slug validation
     - test_valid_slug_passes()
     - test_invalid_project_slug_error()
   - **Run**: pytest → EXPECT RED
   - **GREEN**: Implement validate_slug() function
   - **Run**: pytest → EXPECT GREEN
   - **Validate**: pytest → STAY GREEN
   - **Commit**: "feat: Add project slug validation with tests\n\nRefs: TEST-123"

4. Hook Integration
   - **RED**: Write integration test
     - test_pre_gen_hook_calls_validator()
   - **Run**: pytest → EXPECT RED
   - **GREEN**: Modify hooks/pre_gen_project.py to call validator
   - **Run**: pytest → EXPECT GREEN
   - **Validate**: pytest + manual cookiecutter test → STAY GREEN
   - **Commit**: "feat: Integrate validator into pre-gen hook with tests\n\nRefs: TEST-123"

5. Documentation
   - Update README.md with validation feature
   - Add docstrings to all functions
   - Commit: "docs: Document cookiecutter validation feature\n\nRefs: TEST-123"

**Note:** Each unit follows strict TDD cycle: Write failing tests first, implement to make them pass, validate against existing tests.

---

Do you approve this plan?

[If user says NO or requests changes]:
- Stay in plan mode
- Make requested revisions
- Present updated plan
- Ask again: "Do you approve this plan?"

[If user says YES or approves]:

✅ **Plan approved.**

**To implement this plan, run:** `/devflow:implement`

**To make changes to the plan:** Provide your feedback and I'll revise it.

**DO NOT proceed with implementation.** The `/devflow:implement` command handles all implementation work.

[Then stop - do not call ExitPlanMode, do not start implementing, just end the response naturally]
