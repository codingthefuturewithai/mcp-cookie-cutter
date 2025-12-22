---
description: Analyze JIRA issue and develop implementation plan
argument-hint: "[--tdd] [ISSUE-KEY]"
allowed-tools: ["mcp__atlassian__getJiraIssue", "mcp__atlassian__getAccessibleAtlassianResources", "Grep", "Glob", "Read", "Bash", "mcp__context7__resolve-library-id", "mcp__context7__get-library-docs", "Write"]
---

# Plan Work

I'll analyze issue $ARGUMENTS and create a detailed implementation plan.

---

## Step 1: Fetch JIRA Issue

Let me fetch the full issue details from JIRA.

## Note for AI Assistants - FETCH PHASE

1. Use `mcp__atlassian__getAccessibleAtlassianResources` to get cloud ID
2. Use `mcp__atlassian__getJiraIssue` with $ARGUMENTS to fetch full issue details
3. Extract: Summary, Description, Acceptance Criteria, Issue Type
4. Check if $ARGUMENTS contains --tdd flag (if yes: TDD Mode ENABLED; if no: DISABLED)
5. Proceed to Step 2

---

## Step 2: Analyze Codebase

Based on the issue requirements, let me analyze the existing codebase.

## Note for AI Assistants - ANALYSIS PHASE

**Codebase Analysis:**
- Use Grep/Glob to search for related code
- Identify existing patterns (imports, error handling, logging, structure)
- Find integration points
- Document code patterns to follow

**If TDD Mode is ENABLED:**
- Detect test framework (pytest, jest, JUnit, RSpec, etc.)
- Search for test directories: tests/, test/, spec/, __tests__/
- Read 2-3 test files to extract patterns
- Map existing tests to components that will be modified
- Identify test commands: run all tests, run specific test

After gathering this information, proceed to Step 3.

---

## Step 3: Research with Context7

Now I'll research relevant technologies, libraries, and frameworks to ensure we follow current best practices.

## Note for AI Assistants - RESEARCH PHASE

**ALWAYS use Context7 research when:**
- Issue involves implementing a new feature (research the domain/approach)
- Issue mentions ANY specific library or framework (research current docs)
- Issue requires integration with external services/APIs
- Issue involves a technology you need current best practices for
- Issue type is Feature, Story, or Epic

**For each technology/library identified:**
1. Use `mcp__context7__resolve-library-id` to identify the library
2. Use `mcp__context7__get-library-docs` to fetch current documentation
3. Document in your analysis:
   - Current best practices and recommended patterns
   - Version-specific considerations
   - Common pitfalls to avoid
   - Integration patterns relevant to this codebase

**Skip Context7 research ONLY when:**
- Issue is a simple bug fix in existing code
- Issue is refactoring with no new dependencies
- Issue is documentation-only changes

After research, proceed to Step 4.

---

## Step 4: Present Draft Plan for Approval

Based on my analysis, here's the proposed implementation plan for $ARGUMENTS:

**Issue Summary:**
[Issue type, summary, key requirements]

**Acceptance Criteria:**
[Breakdown of each criterion]

**Codebase Analysis:**
[Existing patterns found, integration points, files to modify]

**Implementation Plan:**
1. Files to create/modify: [specific paths]
2. Functions/components to implement: [details]
3. Code patterns to follow: [from codebase analysis]
4. Integration approach: [how it connects]

**Testing Strategy:**
[Test framework, test cases, coverage approach]

**If TDD Mode:**
- Test framework detected: [pytest/jest/etc.]
- Existing test patterns: [from analysis]
- Test cases from acceptance criteria: [specific tests]
- RED/GREEN/REFACTOR workflow:
  1. RED: Write failing tests for [feature]
  2. GREEN: Implement minimal code to pass
  3. REFACTOR: Clean up and optimize
  4. VALIDATE: Run full test suite
- Test commands:
  - Run all: [command]
  - Run specific: [command]

**Context7 Research:**
[Best practices, patterns, version notes - if applicable]

**Documentation Updates:**
[Files to update: README, docs/, code comments]

**Commit Strategy:**
1. [Logical unit 1] - refs $ARGUMENTS
2. [Logical unit 2] - refs $ARGUMENTS
3. [etc.]

---

**Does this plan look good? Would you like any changes?**

You can:
- Type **"yes"** or **"approved"** to finalize and save the plan
- Request changes like **"add more detail to testing"** or **"research authentication patterns"**
- Ask questions about any part of the plan

Take your time to review - we'll iterate until you're satisfied.

## Note for AI Assistants - APPROVAL PHASE

[WAIT FOR USER RESPONSE BEFORE CONTINUING]

**After user responds:**

- **If user approves** (says "yes", "approved", "looks good", "go ahead", "lgtm", "ship it", etc.):
  - Acknowledge approval
  - Proceed to Step 5
  - Write the final plan to `.devflow/plans/$ARGUMENTS.md`

- **If user requests changes** (says "change X", "add Y", "remove Z", "make it more detailed", "research [technology]", etc.):
  - Acknowledge their feedback
  - Re-analyze codebase if they want more technical details
  - Re-research with Context7 if they mention new technologies/patterns
  - Revise the specific sections they mentioned
  - Present the COMPLETE revised plan using the same format as above
  - Ask the same approval question again: "Does this plan look good? Would you like any changes?"
  - [WAIT FOR USER RESPONSE BEFORE CONTINUING]
  - Repeat this cycle until they explicitly approve

- **If user asks questions** (seeks clarification about approach, asks "why X", etc.):
  - Answer their questions thoroughly
  - Offer to revise the plan if needed based on the discussion
  - [WAIT FOR USER RESPONSE BEFORE CONTINUING]

**CRITICAL:** Do NOT proceed to Step 5 until user explicitly approves with phrases like "yes", "approved", "looks good", "go ahead", "lgtm", etc.

---

## Step 5: Save Approved Plan

✅ **Plan approved!**

Now I'll save the final plan to `.devflow/plans/$ARGUMENTS.md`

## Note for AI Assistants - SAVE PHASE

Use the Write tool to create `.devflow/plans/$ARGUMENTS.md` with the complete plan including all sections:
- Issue Summary
- Acceptance Criteria
- Codebase Analysis
- Implementation Plan
- Testing Strategy (with TDD workflow if enabled)
- Context7 Research (if performed)
- Documentation Updates
- Commit Strategy

After writing the file, proceed to Step 6.

---

## ✅ Planning Complete

Your implementation plan has been saved to: `.devflow/plans/$ARGUMENTS.md`

---

## 📋 What Happens Next?

**You have 2 options:**

### Option 1: Implement the Plan
Run the implement command to start coding:
```bash
/devflow:implement $ARGUMENTS
```

This will:
- Create a feature branch for $ARGUMENTS
- Update JIRA status to "In Progress"
- Implement the code following your approved plan
- Run tests (TDD workflow if --tdd was used)
- Create commits referencing $ARGUMENTS
- Prepare for PR creation

### Option 2: Revise the Plan
If you thought of improvements, just tell me what to change:
- "Add more detail about error handling"
- "Research [library] for the authentication part"
- "Include database migration steps"

I'll update `.devflow/plans/$ARGUMENTS.md` and present the revised version.

---

## 🛑 Planning Phase Complete

**This command has finished its job.** The plan is saved and ready for implementation.

**No code has been written.** This command ONLY creates plans - the `/devflow:implement` command handles all code changes, testing, commits, and PR creation.

---

## Note for AI Assistants - COMMAND COMPLETE

**This command is FINISHED. Stop here.**

Do NOT:
- Implement any code
- Create branches
- Make commits
- Update JIRA
- Create pull requests
- Use Edit or MultiEdit tools

The `/devflow:implement` command will handle all implementation tasks.
