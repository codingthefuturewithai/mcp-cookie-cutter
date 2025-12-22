---
description: Execute approved implementation plan
argument-hint: "[ISSUE-KEY]"
allowed-tools: ["Read", "Write", "Edit", "Bash", "Grep", "Glob", "TodoWrite", "mcp__atlassian__getTransitionsForJiraIssue", "mcp__atlassian__transitionJiraIssue"]
---

# Implement Work

I'll execute the approved implementation plan for $ARGUMENTS.

**Prerequisites:**
- Approved plan at `.devflow/plans/$ARGUMENTS.md`
- Run `/devflow:plan-work $ARGUMENTS` if plan doesn't exist

---

## Step 0: Load Implementation Plan

Let me load the approved plan for $ARGUMENTS.

## Note for AI Assistants - LOAD PLAN PHASE

1. Use Read tool to load `.devflow/plans/$ARGUMENTS.md`
2. If file doesn't exist:
   - ❌ ERROR: "No implementation plan found for $ARGUMENTS"
   - Tell user: "Please run `/devflow:plan-work $ARGUMENTS` first to create a plan"
   - STOP - cannot proceed without approved plan
3. Extract from plan:
   - Issue summary and type
   - Implementation steps and approach
   - Files to create/modify
   - Testing strategy and test cases
   - TDD workflow sections (if present)
   - Documentation files to update
   - Commit strategy
4. Detect TDD Mode:
   - Search plan content for "RED/GREEN/REFACTOR workflow" section
   - If present → TDD Mode ENABLED
   - If absent → TDD Mode DISABLED
5. Store extracted plan details for reference throughout implementation
6. Proceed to Step 1

[Read the plan file and extract key information]

---

✅ **Plan loaded:** `.devflow/plans/$ARGUMENTS.md`

**Issue:** [Issue type from plan] - [Summary from plan]

**TDD Mode:** [ENABLED if RED/GREEN/REFACTOR workflow found in plan, DISABLED otherwise]

**Implementation approach:** [Brief summary from plan]

---

## Step 1: Create Git Branch

**Check if git repository exists:**

```bash
git rev-parse --git-dir 2>/dev/null || echo "not-a-repo"
```

**If not a git repository:**

Initialize git and create initial commit:

```bash
git init
git add .
git commit -m "Initial commit" || echo "Nothing to commit yet"
```

✅ Git initialized

**Determine branch type:**
- Feature/Executable Spec → `feature/[ISSUE-KEY]-[slug]`
- Bug → `bugfix/[ISSUE-KEY]-[slug]`
- Other → `task/[ISSUE-KEY]-[slug]`

**Create branch:**

```bash
git checkout -b [branch-name]
```

✅ Branch: [branch-name]

---

## Step 2: Update JIRA Status

[Call `mcp__atlassian__getTransitionsForJiraIssue`]
[Call `mcp__atlassian__transitionJiraIssue` to "In Progress"]

✅ JIRA: In Progress

---

**TDD Mode:** [Set in Step 0 based on plan content]

[If TDD mode enabled]:
✅ TDD Mode enabled - Following RED/GREEN/REFACTOR workflow from approved plan

[If TDD mode disabled]:
Standard implementation workflow (implementation first, then tests)

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
Following the approved plan's implementation steps and validation strategy.

### For Each Logical Unit (from approved plan):

**1. Implement Changes**

Create/modify files as specified in the approved plan, following discovered code patterns.

**Files to modify (from plan):** [List from plan's Implementation Plan section]

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

Commit after validation passes, following the commit strategy from the approved plan:
- Reference issue key ($ARGUMENTS)
- Describe what was done
- Note validation status
- Follow commit message format from plan

**5. Report Progress**

✅ Unit complete: [description]
Validation: [test results / verification method]
Docs: [what was updated]

---

[If TDD Mode is ENABLED]:
Following Test-Driven Development workflow from approved plan.

**Test framework detected in plan:** [Framework from plan's Testing Strategy]
**Test patterns to follow:** [Patterns documented in plan]

### For Each Logical Unit (from approved plan):

---

**STEP 1: Write Failing Tests (RED Phase)**

Before writing ANY implementation code:

Creating test file: tests/[unit|integration]/test_[component].py

Following test patterns documented in approved plan:
- [Pattern 1 from plan: e.g., using pytest fixtures]
- [Pattern 2 from plan: e.g., class-based test organization]
- [Pattern 3 from plan: e.g., mock external dependencies with unittest.mock]

Writing tests for behaviors specified in plan's test cases:
- [Test case 1 from plan's TDD workflow]
- [Test case 2 from plan's TDD workflow]
- [Test case 3 from plan's TDD workflow]
- [Additional edge cases from plan]

[Use Write or Edit tool to create test file]

**Verify tests fail correctly:**
```bash
[Use test command from plan's TDD workflow section]
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

Following commit strategy from approved plan:

```bash
git add [test files] [implementation files] [documentation files]
git commit -m "feat|fix|docs: [unit description]

- Add tests for [behaviors tested]
- Implement [what was implemented]
- Update [documentation updated]

Refs: $ARGUMENTS"
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

Please run `/devflow:plan-work $ARGUMENTS` to revise the plan, then return to `/devflow:implement $ARGUMENTS`.

DO NOT continue implementation - the plan at `.devflow/plans/$ARGUMENTS.md` must be updated first.

---

## Implementation Summary

**Plan executed:** `.devflow/plans/$ARGUMENTS.md`

**Completed:**
- [X] logical units implemented (from plan)
- [Y] validations passing
- [Z] documentation files updated
- [N] commits created

**Files Modified:**
[List with paths - compare with plan's expected files]

**Plan adherence:** [Brief note on any deviations from approved plan]

---

## ✅ Implementation Complete

All tasks from the approved plan have been implemented and validated.

---

## 🔒 Security Review (Recommended)

**Before creating your PR, consider running a security analysis:**

```bash
/devflow:security-review $ARGUMENTS
```

This is especially important if you modified:
- Authentication/authorization logic
- Input validation or API integrations
- Database queries or file operations
- Cryptographic functions or dependencies

Skip if: Documentation-only changes or low-risk refactoring

---

**Next step:**

Run the complete command to finalize:
```bash
/devflow:complete $ARGUMENTS
```

This will:
- Run final full test suite validation
- Create pull request with all commits
- Update JIRA status to "Ready for Review"
- Link PR to JIRA issue

**DO NOT CONTINUE** - User must run `/devflow:complete $ARGUMENTS` to finalize
