---
description: Execute approved plan with validation and documentation
argument-hint: "[--tdd]"
allowed-tools: ["Read", "Write", "Edit", "Bash", "Grep", "Glob", "TodoWrite", "EnterPlanMode", "ExitPlanMode"]
---

# Implement Work

I'll execute the approved plan with validation, documentation updates, and incremental commits.

**Prerequisites:** Approved plan from `/devflow:plan-work`

---

## Step 0: Exit Plan Mode (if needed)

[If currently in plan mode from `/devflow:plan-work`]:

[Call `ExitPlanMode`]

This will prompt you to choose how to proceed with implementation.

---

[Check if --tdd flag was used in plan-work or if passed to this command]

**TDD Mode:** [If --tdd present: ENABLED | If absent: DISABLED]

[If --tdd mode enabled, notify user]:
✅ TDD Mode enabled - Following RED/GREEN/REFACTOR workflow

[If --tdd mode disabled]:
Standard implementation workflow (tests after code)

---

## Critical Requirements

**Test Pattern Compliance (when tests required):**
- Discover existing test files in repository
- Study their structure, naming, organization, assertions
- Follow those patterns exactly
- Do NOT create tests in different style

**Code Pattern Compliance (always):**
- Follow import patterns from existing code
- Follow error handling conventions
- Follow logging patterns
- Follow module structure and organization
- Maintain modular design

**Documentation Updates (always):**
- Search repository for all documentation files
- Identify documentation affected by changes
- Update all relevant documentation
- Update code comments and docstrings

---

## Implementation Process

[If TDD Mode is DISABLED]:
Following the approved plan's validation strategy.

### For Each Logical Unit:

**1. Implement Changes**

Create/modify files as specified in plan following discovered patterns.

**2. Validate Changes**

[Strategy from plan - adapts to work type]:

**For code with tests:**
- Study existing test patterns
- Generate tests following those patterns
- Run tests for this unit

**For bug fixes:**
- Create regression test
- Verify bug no longer reproduces
- Run affected tests

**For infrastructure/config:**
- Trigger workflow or process
- Verify expected behavior
- Check logs/output

**For documentation:**
- Review accuracy
- Test code examples
- Verify links

**3. Update Documentation**

- Search for affected documentation files
- Update as needed
- Update code comments

**4. Commit Validated Unit**

Commit after validation passes:
- Reference issue key
- Describe what was done
- Note validation status

**5. Report Progress**

✅ Unit complete: [description]
Validation: [test results / verification method]
Docs: [what was updated]

---

[If TDD Mode is ENABLED]:
Following Test-Driven Development workflow from approved plan.

### For Each Logical Unit:

---

**STEP 1: Write Failing Tests (RED Phase)**

Before writing ANY implementation code:

Creating test file: tests/[unit|integration]/test_[component].py

Following discovered patterns from plan:
- [Pattern 1: e.g., using pytest fixtures]
- [Pattern 2: e.g., class-based test organization]
- [Pattern 3: e.g., mock external dependencies with unittest.mock]

Writing tests for:
- [Behavior 1 from acceptance criteria]
- [Behavior 2 from acceptance criteria]
- [Edge case]
- [Error condition]

[Use Write or Edit tool to create test file]

**Verify tests fail correctly:**
```bash
[framework-specific command to run just these tests]
```

Expected: Tests fail with "not implemented" or assertion errors
Actual: [report actual result]

⚠️ **If tests fail for wrong reason** (syntax error, import error, indentation):

**Auto-fix attempt:**
1. Check error message for common issues:
   - Missing imports → Add import statements
   - Syntax errors → Fix missing colons, parentheses, brackets
   - Indentation errors → Correct indentation
   - Undefined names → Add imports or fix typos

2. Apply fix using Edit tool

3. Re-run tests

4. If still failing for wrong reason:
   → Report error to user
   → Wait for guidance
   → DO NOT proceed to implementation

✅ **Tests failing for right reason** (functionality not implemented yet)

---

**STEP 2: Implement Code (GREEN Phase)**

Now implementing to make tests pass:

[Create/modify implementation files using Write/Edit tools]

**Run tests - expect GREEN:**
```bash
[same test command from RED phase]
```

Expected: All new tests pass
Actual: [report results]

❌ **If tests still failing:**
  → Debug implementation
  → Fix code
  → Re-run tests
  → Repeat until green

✅ **All new tests passing**

---

**STEP 3: Run Relevant Existing Tests**

Verify we didn't break existing functionality.

**Auto-run recommended test subset** (from plan):
```bash
[command to run MUST_RUN + SHOULD_RUN tests from plan]
```

Expected: All relevant existing tests pass
Actual: [report results with count and timing]

⚠️ **If existing tests fail:**
  → **Regression detected!**
  → Show which tests failed
  → Fix implementation to maintain backward compatibility
  → Re-run all tests (new + existing)
  → Repeat until all green

✅ **All tests passing** (new tests: [X], existing tests: [Y])

**User override available:**
If user says "run full suite" or "skip existing tests", adjust accordingly.

---

**STEP 4: Refactor (if needed)**

[Only if code quality improvements needed]

Improving code quality:
- [Refactoring action 1: e.g., extract helper function]
- [Refactoring action 2: e.g., improve naming]
- [Refactoring action 3: e.g., remove duplication]

**Run tests after refactoring:**
```bash
[command to run new tests + relevant existing tests]
```

Expected: All tests still pass
Actual: [report results]

✅ **Tests still green after refactoring**

---

**STEP 5: Update Documentation**

[Search for affected documentation files using Glob]

Affected documentation:
- [path/to/doc1.md] - [what needs updating]
- [path/to/doc2.md] - [what needs updating]

[Update each file]

Updated:
- [file]: [description of changes]

---

**STEP 6: Commit Validated Unit**

```bash
git add [test files] [implementation files] [documentation files]
git commit -m "feat|fix|docs: [unit description]

- Add tests for [behaviors tested]
- Implement [what was implemented]
- Update [documentation updated]

Refs: [ISSUE-KEY]"
```

✅ **Unit complete and committed**

Commit: [commit hash]
Files changed: [count]
Tests: [X new, Y passing total]

---

[Repeat TDD cycle for next logical unit...]

---

## Auto Re-plan When Needed

If major deviation from plan required (including when tests reveal issues):

⚠️ **STOP - Major Deviation Detected**

Discovered during [implementation|testing]: [problem]
[If TDD Mode: Test results show: [what tests revealed]]
Cannot proceed because: [reason]

**Action required:** The current plan needs significant revision.

Please run `/devflow:plan-work [ISSUE-KEY]` to revise the plan, then return to `/devflow:implement`.

DO NOT continue implementation - plan must be updated first.

---

## Implementation Summary

**Completed:**
- [X] logical units implemented
- [Y] validations passing
- [Z] documentation files updated
- [N] commits created

**Files Modified:**
[List with paths]

---

## ⛔ STOP - Ready for Final Validation

Implementation complete.

**Next step:**
```
/complete [ISSUE-KEY]
```

This will run final validation, create PR, and update JIRA.

DO NOT CONTINUE - User must run `/complete`
