---
description: Execute approved implementation plan
argument-hint: "[--auto] [ISSUE-KEY]"
allowed-tools: ["Read", "Write", "Edit", "Bash", "Grep", "Glob", "TodoWrite", "mcp__atlassian__getAccessibleAtlassianResources", "mcp__atlassian__getJiraIssue", "mcp__atlassian__getTransitionsForJiraIssue", "mcp__atlassian__transitionJiraIssue"]
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
6. **Parse $ARGUMENTS for flags:**
   - Check if $ARGUMENTS contains ` --auto` (with spaces around it)
   - If found: AUTO_MODE = true, strip `--auto` from ISSUE_KEY
   - If not found: AUTO_MODE = false, ISSUE_KEY = $ARGUMENTS
   - Store AUTO_MODE for reference throughout execution
7. **Count logical units from plan:**
   - Search for "Unit X of Y" pattern in plan's Incremental Implementation Schedule
   - Extract Y as TOTAL_UNITS
   - Fallback to counting "### Commit" or numbered list if new format not found
   - If no clear pattern, default to "?" for unknown total
   - Store TOTAL_UNITS for progress tracking
8. **Initialize progress tracking:**
   - Set CURRENT_UNIT = 0
   - Will increment after each unit completion
9. Proceed to Step 1

## Note for AI Assistants - FLAG DETECTION & COUNTING

After loading the plan file:

**1. Detect auto mode:**
```bash
# Check for --auto flag in $ARGUMENTS
if [[ "$ARGUMENTS" == *" --auto"* ]] || [[ "$ARGUMENTS" == *"--auto "* ]]; then
    AUTO_MODE="true"
    ISSUE_KEY="${ARGUMENTS//--auto/}"
    ISSUE_KEY="${ISSUE_KEY// /}"  # Remove extra spaces
else
    AUTO_MODE="false"
    ISSUE_KEY="$ARGUMENTS"
fi
```

**2. Count logical units:**
```bash
# Extract total from "Unit X of Y" pattern in plan
# First try new format: "### Unit 1 of 5"
TOTAL_UNITS=$(grep -oP "Unit \d+ of \K\d+" ".devflow/plans/$ISSUE_KEY.md" 2>/dev/null | head -1)

# Fallback to old format if new format not found
if [ -z "$TOTAL_UNITS" ]; then
    TOTAL_UNITS=$(grep -c "^### Commit [0-9]" ".devflow/plans/$ISSUE_KEY.md" 2>/dev/null || grep -c "^[0-9]\." ".devflow/plans/$ISSUE_KEY.md" 2>/dev/null || echo "?")
fi
```

**3. Initialize tracking:**
- Set CURRENT_UNIT=0
- Store AUTO_MODE and TOTAL_UNITS for later reference

[Read the plan file and extract key information]

---

✅ **Plan loaded:** `.devflow/plans/$ARGUMENTS.md`

**Issue:** [Issue type from plan] - [Summary from plan]

**TDD Mode:** [ENABLED if RED/GREEN/REFACTOR workflow found in plan, DISABLED otherwise]

**Auto-mode:** [ENABLED if --auto detected in $ARGUMENTS, DISABLED otherwise]

[If auto-mode ENABLED]: Will run all [TOTAL_UNITS] logical units continuously without pausing

[If auto-mode DISABLED]: Will pause after each logical unit for review and approval

**Progress:** Unit 1 of [TOTAL_UNITS] commits
**Each commit = 1 mandatory pause point**
**After this unit: STOP and wait for approval**

**Implementation approach:** [Brief summary from plan]

---

## ⚠️ MANDATORY: PAUSE AFTER EVERY COMMIT

**NON-NEGOTIABLE RULE:**
- Each commit in the plan = exactly ONE pause point
- After EVERY commit: generate summary + stop + wait for user response
- Do NOT proceed to next unit without explicit user approval

**If plan has 3 commits → you will pause 3 times**
**If plan has 5 commits → you will pause 5 times**

**This applies to ALL modes including TDD (RED/GREEN/REFACTOR).**

**Exception:** If AUTO_MODE is true (--auto flag), skip all pauses and run continuously.

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

## Note for AI Assistants - JIRA UPDATE

**Check current status first, then transition if needed:**

1. Call `mcp__atlassian__getAccessibleAtlassianResources` to get cloud ID
2. Extract cloudId from the response (first item in array)

3. Call `mcp__atlassian__getJiraIssue` with:
   - cloudId
   - issueIdOrKey = $ARGUMENTS
   - fields = ["status"]

4. Extract current status from response: `fields.status.name`

5. **If current status is already "In Progress":**
   - Skip transition (already set)
   - Display: "✅ JIRA: In Progress (already set)"
   - Proceed to next step

6. **If current status is NOT "In Progress":**
   - Call `mcp__atlassian__getTransitionsForJiraIssue` with cloudId and issue key
   - Find transition where `to.name` equals "In Progress"
   - Extract the `id` field from that transition (e.g., "21")
   - Call `mcp__atlassian__transitionJiraIssue` with:
     ```json
     {
       "cloudId": "[cloudId]",
       "issueIdOrKey": "$ARGUMENTS",
       "transition": { "id": "[transition_id]" }
     }
     ```
   - Display: "✅ JIRA: In Progress"

**IMPORTANT:** The `to.name` field in transitions shows the DESTINATION status, not the current status. Don't confuse seeing "In Progress" in the transitions list with the issue already being in that status.

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

**5. Generate Unit Summary**

Analyzing what was implemented in this unit...

## Note for AI Assistants - GENERATE SUMMARY

Use Bash to get commit details:
```bash
# Get the latest commit details
git log -1 --format="%h%n%s%n%b"

# Get files changed in this commit
git diff-tree --no-commit-id --name-status HEAD
```

Analyze the commit diff and describe what actually changed:
- For test files: what behaviors are being tested?
- For implementation files: what functionality was added/modified?
- For documentation: what was documented?

Present the analysis in the Unit Summary below.

---

**Unit Summary:**

**Unit [CURRENT_UNIT + 1] of [TOTAL_UNITS]**

- **Commit:** [short hash] - [commit message]
- **Files changed:** [count] files
  - [path/to/file1.ext] - [Added/Modified/Deleted]
  - [path/to/file2.ext] - [Added/Modified/Deleted]
  - [... list all files ...]
- **Tests:** [X total passing] ([if new tests]: +Y new tests)
- **What changed:**
  - **Testing:** [Describe test behaviors if test files were added/modified, or "None" if no tests]
  - **Implementation:** [Describe functionality that was added or modified]
  - **Documentation:** [Describe what was documented, or "None" if no doc changes]

---

[If AUTO_MODE is false]:

**6. Review and Approval**

This completes Unit [CURRENT_UNIT + 1] of [TOTAL_UNITS].

**What would you like to do?**

- Type **"continue"** or **"next"** → Proceed to next logical unit
- Type **"review [filename]"** → Inspect a specific file
- Type **"revise [instructions]"** → Make changes to this unit before continuing
- Type **"stop"** → Stop implementation here (all work so far is committed)

## Note for AI Assistants - APPROVAL HANDLING

[WAIT FOR USER RESPONSE BEFORE CONTINUING]

**After user responds:**

- **If "continue", "next", "yes", "ok", "proceed", "go ahead"**:
  - Increment CURRENT_UNIT by 1
  - If CURRENT_UNIT < TOTAL_UNITS: proceed to next logical unit (loop back to step 1)
  - If CURRENT_UNIT >= TOTAL_UNITS: proceed to Implementation Summary section

- **If "review [filename]"**:
  - Use Read tool to show the requested file
  - Re-display the "What would you like to do?" question
  - [WAIT FOR USER RESPONSE BEFORE CONTINUING]

- **If "revise [instructions]"**:
  - Acknowledge: "I'll revise [what they asked for]"
  - Use Edit tool to make the requested changes
  - Re-run validation (tests if applicable)
  - Show new validation results
  - Amend the commit: `git commit --amend --no-edit` (or with updated message if needed)
  - Re-generate and display the unit summary with updated information
  - Re-ask: "What would you like to do?"
  - [WAIT FOR USER RESPONSE BEFORE CONTINUING]
  - Track revision attempts (warn after 3 attempts)

- **If "stop", "exit", "halt", "done"**:
  - Acknowledge: "Stopping implementation. All completed work has been committed."
  - Show summary: "[CURRENT_UNIT + 1] of [TOTAL_UNITS] logical units completed"
  - Skip remaining units
  - Proceed to Implementation Summary section

---

[If AUTO_MODE is true]:
[Skip approval section entirely, increment CURRENT_UNIT, and immediately proceed to next logical unit or Implementation Summary]

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

**STEP 7: Generate TDD Cycle Summary**

Analyzing what was delivered in this TDD cycle...

## Note for AI Assistants - GENERATE TDD SUMMARY

Use Bash to get commit details:
```bash
# Get the latest commit details
git log -1 --format="%h%n%s%n%b"

# Get files changed in this commit
git diff-tree --no-commit-id --name-status HEAD
```

Analyze the commit diff and describe what was delivered in each TDD phase:
- **RED phase:** What test behaviors were specified?
- **GREEN phase:** What functionality was implemented to make tests pass?
- **REFACTOR phase:** What improvements were made (if any)?
- **Documentation:** What was documented?

Present the analysis in the TDD Cycle Summary below.

---

**TDD Cycle Summary:**

**Unit [CURRENT_UNIT + 1] of [TOTAL_UNITS]**

- **Commit:** [short hash] - [commit message]
- **Files changed:** [count] files
  - **Tests:**
    - [path/to/test_file1.py] - [Added/Modified/Deleted]
  - **Implementation:**
    - [path/to/impl_file1.py] - [Added/Modified/Deleted]
  - **Documentation:**
    - [path/to/doc_file1.md] - [Added/Modified/Deleted]
- **Test Results:** [X new tests passing], [Y total tests passing]
- **What was delivered:**
  - **RED phase:** [Describe test behaviors that were specified]
  - **GREEN phase:** [Describe implementation that makes tests pass]
  - **REFACTOR phase:** [Describe any code quality improvements, or "None" if skipped]
  - **Documentation:** [Describe what was documented, or "None" if no doc changes]

---

[If AUTO_MODE is false]:

**STEP 8: Review and Approval**

This completes TDD Cycle [CURRENT_UNIT + 1] of [TOTAL_UNITS].

**What would you like to do?**

- Type **"continue"** or **"next"** → Proceed to next TDD cycle
- Type **"review [filename]"** → Inspect a specific file
- Type **"revise [instructions]"** → Make changes to this cycle before continuing
- Type **"stop"** → Stop implementation here (all work so far is committed)

## Note for AI Assistants - TDD APPROVAL HANDLING

[WAIT FOR USER RESPONSE BEFORE CONTINUING]

**After user responds:**

- **If "continue", "next", "yes", "ok", "proceed", "go ahead"**:
  - Increment CURRENT_UNIT by 1
  - If CURRENT_UNIT < TOTAL_UNITS: proceed to next TDD cycle (loop back to STEP 1: Write Failing Tests)
  - If CURRENT_UNIT >= TOTAL_UNITS: proceed to Implementation Summary section

- **If "review [filename]"**:
  - Use Read tool to show the requested file
  - Re-display the "What would you like to do?" question
  - [WAIT FOR USER RESPONSE BEFORE CONTINUING]

- **If "revise [instructions]"**:
  - Acknowledge: "I'll revise [what they asked for]"
  - Use Edit tool to make the requested changes
  - Re-run tests (both new and relevant existing tests)
  - Show new test results
  - Amend the commit: `git commit --amend --no-edit` (or with updated message if needed)
  - Re-generate and display the TDD Cycle Summary with updated information
  - Re-ask: "What would you like to do?"
  - [WAIT FOR USER RESPONSE BEFORE CONTINUING]
  - Track revision attempts (warn after 3 attempts)

- **If "stop", "exit", "halt", "done"**:
  - Acknowledge: "Stopping implementation. All completed TDD cycles have been committed."
  - Show summary: "[CURRENT_UNIT + 1] of [TOTAL_UNITS] TDD cycles completed"
  - Skip remaining cycles
  - Proceed to Implementation Summary section

---

[If AUTO_MODE is true]:
[Skip approval section entirely, increment CURRENT_UNIT, and immediately proceed to next TDD cycle or Implementation Summary]

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

**Progress:** [CURRENT_UNIT] of [TOTAL_UNITS] logical units completed

**Mode:** [Auto-mode ENABLED / Auto-mode DISABLED - paused after each unit]

**Completed:**
- [CURRENT_UNIT] logical units implemented (from plan)
- [Y] validations passing
- [Z] documentation files updated
- [CURRENT_UNIT] commits created (one per logical unit)

**Files Modified:**
[List with paths - compare with plan's expected files]

**Plan adherence:** [Brief note on any deviations from approved plan]

---

## ✅ Implementation Complete

All tasks from the approved plan have been implemented and validated.

---

## 🔒 Security Review (Recommended)

**You have two options:**

### Option 1: Run Security Scan First (Recommended)

Scan your changes for OWASP Top 10 vulnerabilities:

```bash
/devflow:security-review $ARGUMENTS
```

This is especially important if you modified:
- Authentication/authorization logic
- Input validation or API integrations
- Database queries or file operations
- Cryptographic functions or dependencies

After the scan completes, you'll be prompted to run `/devflow:complete`.

---

### Option 2: Skip Security Scan and Create PR

If you prefer to skip the security scan (e.g., documentation-only changes):

```bash
/devflow:complete $ARGUMENTS
```

This will:
- Run final full test suite validation
- Create pull request with all commits
- Update JIRA status to "Done"
- Link PR to JIRA issue

---

**DO NOT CONTINUE** - User must choose one of the options above to finalize
