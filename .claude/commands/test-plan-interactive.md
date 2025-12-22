---
description: Test interactive planning with user approval
argument-hint: "[--tdd]"
allowed-tools: ["Grep", "Glob", "Read", "Bash", "Write"]
---

# Plan Work - Interactive Test (TEST-123)

I'll create an implementation plan for TEST-123: Add validation helper for cookiecutter variables.

---

## Mock Issue Details

**Issue:** TEST-123 - Add validation helper for cookiecutter variables
**Type:** Feature

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

**TDD Mode:** [Check if $ARGUMENTS contains --tdd flag - if yes, ENABLED; if no, DISABLED]

---

## Step 1: Analyze Codebase

Let me search for existing validation patterns and understand the current structure.

## Note for AI Assistants - ANALYSIS PHASE

Use Grep/Glob to find:
- Existing validation code in hooks/
- cookiecutter.json structure
- Test patterns if any exist

After gathering this information, proceed to Step 2.

---

## Step 2: Research (if --tdd flag present)

**If TDD Mode is ENABLED:**
- Search for test directories: tests/, test/
- Identify test framework (pytest, unittest, etc.)
- Read 2-3 test files to understand patterns
- Map existing tests to validation components

---

## Step 3: Present Draft Plan for Approval

Based on my codebase analysis, here's the proposed implementation plan:

**Overview:**
[Brief summary of what we're building]

**Files to Create/Modify:**
- [Specific file paths]

**Implementation Approach:**
[How to build it - key functions, logic flow]

**Testing Strategy:**
[Test framework, test cases, coverage approach]

**If TDD Mode:**
[RED/GREEN/REFACTOR workflow phases]

**Commit Strategy:**
[Logical units for commits]

---

**Does this plan look good? Would you like any changes?**

Type "yes" or "approved" to finalize, or tell me what needs to be different.

## Note for AI Assistants - APPROVAL PHASE

[WAIT FOR USER RESPONSE BEFORE CONTINUING]

**After user responds:**

- **If user approves** (says "yes", "approved", "looks good", "go ahead", etc.):
  - Proceed to Step 4
  - Write the final plan to `.devflow/plans/TEST-123.md`

- **If user requests changes** (says "change X", "add Y", "remove Z", etc.):
  - Revise the plan based on their feedback
  - Present the revised plan
  - Ask the same approval question again
  - [WAIT FOR USER RESPONSE BEFORE CONTINUING]
  - Repeat until approved

---

## Step 4: Save Approved Plan

✅ **Plan approved!**

Now I'll save the final plan to `.devflow/plans/TEST-123.md`

[Use Write tool to create the file]

---

## ✅ Planning Complete

Your implementation plan has been saved to: `.devflow/plans/TEST-123.md`

**Next Steps:**

To implement this plan, run:
```
/devflow:implement TEST-123
```

To revise the plan, just tell me what needs to change and I'll update it.

---

## 🛑 CRITICAL COMMAND BOUNDARY

**This command ONLY creates plans - it does NOT implement code.**

Even if the user approved the plan, this command STOPS here. The `/devflow:implement` command handles:
- Branch creation
- JIRA updates
- Code implementation
- Testing
- Commits

**No code will be written by this command under ANY circumstances.**
