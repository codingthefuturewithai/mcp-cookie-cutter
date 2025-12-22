---
description: Create implementation plan ONLY - does NOT implement code
argument-hint: "[--tdd]"
allowed-tools: ["mcp__context7__resolve-library-id", "mcp__context7__get-library-docs", "Read", "Grep", "Glob", "Bash", "Write"]
---

## Plan Work - TEST-123

⚠️ **CRITICAL COMMAND BOUNDARY** ⚠️
- This command MUST ONLY create plans
- This command MUST NOT implement any code
- This command MUST NOT use Edit or MultiEdit tools
- Even if the user says "approved" or "looks good", DO NOT IMPLEMENT

I'll create a detailed implementation plan for TEST-123: Add validation helper for cookiecutter variables.

---

## Mock JIRA Issue Data

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

---

## Step 1: Analyze Codebase

I'll search for existing validation patterns and understand the current structure.

[Use Grep/Glob to find:
- Existing validation code in hooks/
- cookiecutter.json structure
- Test patterns if any exist]

---

## Step 2: Technical Research (if --tdd flag present)

**TDD Mode Enabled:** [Check if $ARGUMENTS contains --tdd]

If TDD mode:
- Search for test directories: tests/, test/
- Identify test framework (pytest, unittest, etc.)
- Read 2-3 test files to understand patterns
- Map existing tests to validation components
- Plan RED/GREEN/REFACTOR workflow

---

## Step 3: Create Implementation Plan

Based on codebase analysis and requirements, I'll present:

1. **Overview** - What we're building
2. **Files to Create/Modify** - Specific paths
3. **Implementation Approach** - How to build it
4. **Testing Strategy** - Test framework, test cases, coverage
5. **TDD Workflow** (if --tdd) - RED/GREEN/REFACTOR phases
6. **Commit Strategy** - Logical units

---

## Step 4: Save Plan and Present

I'll write the complete plan to: `.devflow/plans/TEST-123.md`

Then present a summary here.

---

## 🛑 FULL STOP - Plan Presented

**THIS COMMAND ENDS HERE. I WILL NOT IMPLEMENT ANYTHING.**

After the plan is presented:
1. **You review the plan**
2. **You decide** what to do next

## 🔄 What YOU Must Do Next

**To implement the plan**, YOU must explicitly run:
```
/devflow:implement TEST-123
```

**To revise the plan**:
- Tell me what needs to be different
- I'll revise the plan (still no implementation)

**CRITICAL RULES**:
- Even if you say "approved" → I MUST NOT implement
- Even if you say "looks good" → I MUST NOT implement
- Even if you say "go ahead" → I MUST NOT implement
- ONLY the command `/devflow:implement TEST-123` can trigger implementation

**No code will be written by this command under ANY circumstances.**
