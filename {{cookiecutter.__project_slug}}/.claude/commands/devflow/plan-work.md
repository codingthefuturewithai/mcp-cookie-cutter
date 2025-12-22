---
description: Analyze issue and develop implementation plan
argument-hint: "[--tdd] [ISSUE-KEY]"
allowed-tools: ["mcp__atlassian__getJiraIssue", "mcp__atlassian__getAccessibleAtlassianResources", "Grep", "Glob", "Read", "mcp__context7__resolve-library-id", "mcp__context7__get-library-docs", "EnterPlanMode"]
---

# Plan Work

I'll analyze the issue and develop a detailed implementation plan.

Issue: $ARGUMENTS

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
To enable Test-Driven Development workflow, use: `/devflow:plan-work --tdd [ISSUE-KEY]`

---

## Step 1: Fetch Issue Details

[Call `mcp__atlassian__getAccessibleAtlassianResources`]
[Call `mcp__atlassian__getJiraIssue` with cloudId and issue key]

Issue: [ISSUE-KEY] - [Summary]
Type: [Issue type]

---

## Step 2: Analyze Codebase & Create Implementation Plan

### Analyze Codebase

**Search for related code:**
- Grep/Glob for related components and files
- Read existing implementations to understand patterns
- Identify: import conventions, error handling, logging, module structure
- Find existing tests to understand testing patterns

**Findings:**
- Related files: [paths]
- Code patterns: [import style, error handling, structure]
- Test patterns: [test structure and conventions]
- Integration points: [where this connects]

### Test Strategy Analysis (if --tdd flag present)

[Only if TDD Mode is ENABLED]

**Test Framework Detection:**
[Search codebase to discover test infrastructure - adapt to what exists]

1. **Find test files:**
   - Search for common test directories: tests/, test/, spec/, __tests__/
   - Search for test file patterns: *test*, *spec*, Test*.java, *Tests.cs
   - Check package config: package.json, pom.xml, build.gradle, Gemfile, pyproject.toml, go.mod

2. **Identify frameworks by analyzing what's found:**
   - Read test files to see imports/annotations (pytest, jest, JUnit, NUnit, RSpec, etc.)
   - Check config files for framework declarations
   - Note: May find MULTIPLE frameworks in monorepos (React frontend + Java backend)

3. **Report discovered test infrastructure:**
   - Languages detected: [Python/JavaScript/Java/Go/Ruby/C#/etc.]
   - Frameworks found: [pytest/jest/vitest/JUnit/TestNG/go test/RSpec/etc.]
   - Test locations: [paths to test directories per language]
   - Run commands: [framework-specific commands to run tests]
   - Run specific: [commands to run individual test file/function]

If NO tests found: Note this and skip test mapping (still generate test plan for TDD)

**Existing Test Patterns:**
[Read 2-3 representative test files to extract patterns]

Report discovered patterns:
- File organization: [unit/integration structure, mirrors source or feature-based]
- Test style: [class-based/function-based/describe blocks]
- Assertion style: [assert/expect/should]
- Fixture patterns: [discovered fixture names and usage]
- Mocking approach: [unittest.mock/jest.mock/testify/rspec doubles/etc.]
- Import conventions: [how tests import code under test]

**Relevant Existing Tests:**
[Map ticket components to existing tests]

For each component being modified:

Component: [file/module being changed]
Mapping strategy:
  1. Direct mapping: [src/path → tests/path pattern]
  2. Import analysis: [grep for "import component" in test files]
  3. Naming convention: [ComponentName → test_component_name pattern]

Categorized tests:
  - MUST_RUN: [tests directly testing modified components] (~Xs)
  - SHOULD_RUN: [tests for integration points] (~Xs)
  - Estimated total runtime: ~[X]s vs ~[Y]min full suite

**New Tests Required:**
[Extract testable behaviors from acceptance criteria]

AC #1: "[acceptance criteria text]"
Testable behaviors:
- [Behavior 1: expected outcome]
- [Behavior 2: edge case]
- [Behavior 3: error condition]

Test cases needed:
- test_[behavior_1]()
- test_[behavior_2_edge_case]()
- test_[error_condition]()

AC #2: "[acceptance criteria text]"
Testable behaviors:
- [Behavior: expected outcome]

Test cases needed:
- test_[another_behavior]()

Test files to create:
- tests/[unit|integration]/test_[component].py
  (following [existing_pattern.py] structure)
- tests/[unit|integration]/test_[feature].py
  (following [existing_pattern.py] structure)

**TDD Implementation Order:**
Each logical unit follows: Write tests (RED) → Implement (GREEN) → Refactor → Validate

### Context7 Research (if applicable)

[If issue mentions technologies/libraries]:

Researching: [tech1], [tech2]...

[For each]:
- Call `mcp__context7__resolve-library-id`
- Call `mcp__context7__get-library-docs`

**Research findings:**
- [Tech]: [best practices, current patterns, versions]

### Implementation Plan

[Create plan adapted to issue type]

**For Features:**
- Logical components to build
- Files to create/modify
- Code patterns to follow
- Test strategy
- Integration points

**For Bugs:**
- Reproduction approach
- Investigation strategy
- Root cause hypothesis
- Fix approach with file paths
- Regression test requirement

**For Infrastructure/Config:**
- Files to create/modify
- Validation strategy
- Impact assessment

**For Documentation:**
- Files to update/create
- Accuracy verification approach
- Example testing strategy

**All Plans Include:**

**Code Pattern Compliance:**
- Follow discovered import patterns
- Follow error handling conventions
- Follow logging patterns
- Follow module structure
- Maintain modular design

**Documentation Updates:**
- Search repository for all documentation files
- Identify documentation affected by changes
- Update all relevant documentation
- Update code comments and docstrings

**Validation Strategy:**
[Type-appropriate validation]:
- Features: Unit/integration tests following existing patterns
- Bugs: Regression tests + verification
- Infrastructure: Trigger and verify workflows/configs
- Documentation: Accuracy and example validation

**Commit Strategy:**
- Commit after each logical unit is validated
- Reference issue key in commits

**Implementation Order:**

[If TDD Mode is DISABLED]:
[Sequence of work with rationale]

[If TDD Mode is ENABLED]:
[Sequence with TDD workflow]

**TDD-Enhanced Implementation Order:**

1. [Unit 1 Name]
   - **RED**: Write tests in tests/[unit|integration]/test_[unit].py
     - test_[behavior1]()
     - test_[behavior2]()
     - test_[edge_case]()
   - **Run**: [framework-specific test command] → EXPECT RED (tests fail)
   - **GREEN**: Implement [files to create/modify]
   - **Run**: [same test command] → EXPECT GREEN (tests pass)
   - **Validate**: [command to run relevant existing tests] → STAY GREEN
   - **Commit**: "feat|fix|docs: [unit description] with tests\n\nRefs: [ISSUE-KEY]"

2. [Unit 2 Name]
   - **RED**: Write tests in tests/[unit|integration]/test_[component].py
     - test_[behavior]()
   - **Run**: [test command] → EXPECT RED
   - **GREEN**: Implement [integration code/files]
   - **Run**: [test command] → EXPECT GREEN
   - **Validate**: [relevant unit + integration tests] → STAY GREEN
   - **Commit**: "feat|fix|docs: [unit description] with tests\n\nRefs: [ISSUE-KEY]"

[Continue for all logical units...]

**Note:** Each unit follows strict TDD cycle: Write failing tests first, implement to make them pass, validate against existing tests.

---

## Step 3: Review Plan with User

Do you approve this plan?
