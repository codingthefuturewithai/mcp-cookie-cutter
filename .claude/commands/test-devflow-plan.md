---
description: Test plan-work flow with real analysis on this repo
argument-hint: "[--tdd]"
allowed-tools: ["Grep", "Glob", "Read", "Bash", "EnterPlanMode", "ExitPlanMode", "Write"]
---

# Plan Work - Test Flow

I'll analyze issue TEST-123 and create a detailed implementation plan.

**Your task will be complete when you have created a plan document.** Do not implement any code.

---

## Instructions for Planning

**Issue Details (MOCK DATA):**

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

## Planning Requirements

**TDD Mode:** [Check if $ARGUMENTS contains --tdd flag - if yes, ENABLED; if no, DISABLED]

**Your deliverable is a plan document** that includes:

1. **Codebase Analysis**
   - Search for existing validation code in hooks/
   - Identify test patterns (if any exist)
   - Document code patterns to follow

2. **Implementation Plan**
   - Files to create/modify
   - Functions to implement
   - Test strategy

3. **If TDD Mode is ENABLED:**
   - Detect test framework (pytest, unittest, etc.)
   - Map existing tests to modified components
   - Generate test cases from acceptance criteria
   - Plan RED/GREEN/REFACTOR workflow for each component

4. **Commit Strategy**
   - Logical units for commits
   - Reference issue key in all commits

**Output Format:**
Create your plan as a markdown document at: `.devflow/plans/TEST-123.md`

**Critical:** Your task is COMPLETE when the plan document is created. Do NOT implement any code. The `/devflow:implement` command will execute the plan.

---

## Note for AI Assistants

Enter plan mode and follow these steps:

1. **Explore** the cookiecutter codebase (hooks/, tests/, etc.)
2. **Design** the implementation approach
3. **Create the plan** - Plan mode will create its default plan file
4. **CRITICAL:** After creating the plan, use the Write tool to copy it to `.devflow/plans/TEST-123.md`
5. **Exit** plan mode

Your deliverable is BOTH:
- The plan mode default file (for the 3-option prompt)
- A copy at `.devflow/plans/TEST-123.md` (for /devflow:implement to find)
