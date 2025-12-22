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

Use the Write tool to create `.devflow/plans/$ARGUMENTS.md` with the complete plan including all sections **IN THIS ORDER**:

**1. Mandatory Implementation Rules (FIRST - CRITICAL)**
**2. Issue Summary**
**3. Acceptance Criteria**
**4. Codebase Analysis**
**5. Implementation Plan**
**6. Testing Strategy** (with TDD workflow if enabled)
**7. Context7 Research** (if performed)
**8. Documentation Updates**
**9. Commit Strategy**
**10. Incremental Implementation Schedule (LAST - CRITICAL)**

See detailed templates below for sections 1 and 10.

---

### Template: Section 1 - Mandatory Implementation Rules

This MUST be the first section after the plan title:

```markdown
## ⚠️ MANDATORY IMPLEMENTATION RULES - READ FIRST

**PAUSE AFTER EVERY COMMIT:**
- This plan contains [X] commits = [X] mandatory pause points
- After EACH commit: generate summary, STOP, wait for user approval
- Do NOT proceed to next unit without explicit "continue" response
- If --auto flag: skip pauses and run all units continuously

**Progress Tracking:**
- Current format: "Unit X of [X]"
- Each unit = exactly one commit
- After each unit: STOP and wait for approval (unless --auto)

**Non-Negotiable:**
- [X] commits in this plan = [X] pauses during implementation
- Read the Incremental Implementation Schedule below for explicit pause points

---
```

Replace [X] with the actual number of commits from the Commit Strategy section.

---

### Template: Section 10 - Incremental Implementation Schedule

This MUST be the last section of the plan, after Commit Strategy:

```markdown
## 🔄 Incremental Implementation Schedule

**CRITICAL: Each unit below = ONE mandatory pause point for user review**

**Total Pause Points:** [X]

---

### Unit 1 of [X]: [Commit 1 Title from Commit Strategy]

**Changes:** [Detailed description of what this commit includes]

**Commit message:**
```
[Commit message from Commit Strategy]
```

⏸️ 🛑 **PAUSE POINT #1 - STOP AND WAIT FOR USER APPROVAL**

After committing this unit:
1. Generate unit summary showing what changed
2. Display "What would you like to do?" prompt with options: continue/review/revise/stop
3. STOP and WAIT for user response
4. Only proceed to Unit 2 after explicit approval

---

### Unit 2 of [X]: [Commit 2 Title from Commit Strategy]

**Changes:** [Detailed description of what this commit includes]

**Commit message:**
```
[Commit message from Commit Strategy]
```

⏸️ 🛑 **PAUSE POINT #2 - STOP AND WAIT FOR USER APPROVAL**

After committing this unit:
1. Generate unit summary showing what changed
2. Display "What would you like to do?" prompt with options: continue/review/revise/stop
3. STOP and WAIT for user response
4. Only proceed to Unit 3 after explicit approval

---

[Repeat this structure for ALL commits in the Commit Strategy]

---

### Final Unit [X] of [X]: [Final Commit Title]

**Changes:** [Detailed description]

**Commit message:**
```
[Commit message]
```

⏸️ 🛑 **PAUSE POINT #[X] - FINAL UNIT - STOP AND WAIT FOR USER APPROVAL**

After committing this unit:
1. Generate unit summary showing what changed
2. Display "What would you like to do?" prompt
3. STOP and WAIT for user response
4. After approval: Proceed to Implementation Summary

---
```

**Important:** Number each pause point (PAUSE POINT #1, #2, #3, etc.) and make the visual markers (⏸️ 🛑) prominent.

---

After writing the file with ALL sections in the correct order, proceed to Step 6.

---

## ✅ Planning Complete

Your implementation plan has been saved to: `.devflow/plans/$ARGUMENTS.md`

---

## 📋 What Happens Next?

**You have 2 options:**

### Option 1: Implement the Plan

**By default, implementation pauses after each increment for your review:**

```bash
/devflow:implement $ARGUMENTS
```

This incremental mode will pause after each logical unit (commit) so you can:
- Review what changed (tests, implementation, documentation)
- Approve and continue to next increment
- Request revisions to the current increment
- Review specific files
- Or stop implementation if needed

**OR run all increments continuously without pauses:**

```bash
/devflow:implement --auto $ARGUMENTS
```

Auto mode runs through all logical units from start to finish. Use this when you trust the plan and want hands-off execution.

---

**Which mode should you use?**
- **New to the codebase?** Use default incremental mode to learn as you go
- **Complex feature?** Use incremental mode to catch issues early
- **Simple bug fix?** Use --auto if the plan is straightforward
- **High confidence?** Use --auto for faster execution

---

**What implement does:**
- Create a feature branch for $ARGUMENTS
- Update JIRA status to "In Progress"
- Implement the code following your approved plan
- Run tests (TDD workflow if --tdd was used)
- Create commits referencing $ARGUMENTS
- Prepare for security review and PR creation

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
