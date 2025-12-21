---
description: Fetch JIRA issue and analyze feasibility
argument-hint: "[ISSUE-KEY]"
allowed-tools: ["mcp__atlassian__getJiraIssue", "mcp__atlassian__getAccessibleAtlassianResources", "Grep", "Glob", "Read", "Bash"]
---

# Fetch JIRA Issue & Analyze Feasibility

I'll fetch the JIRA issue and analyze if the work is already done or conflicts exist.

Issue: $ARGUMENTS

---

## Step 1: Fetch Issue from JIRA

[Call `mcp__atlassian__getAccessibleAtlassianResources`]
[Call `mcp__atlassian__getJiraIssue` with cloudId and issue key]

**Issue Summary:**
- **Type**: [Bug/Executable Spec/Task/etc.]
- **Summary**: [Title]
- **Priority**: [Priority]
- **Status**: [Current status]

**Requirements:**
[Key acceptance criteria and objectives]

---

## Step 2: Analyze Feasibility

Searching codebase to determine if work is already done...

**Search Strategy:**
- Grep for keywords from issue title and description
- Grep for function/class/component names mentioned
- Glob for related file structures
- Read relevant files to understand existing implementation
- Check recent git history for related changes

**Feasibility Assessment:**

[Provide one of these outcomes]:

✅ **Not Implemented**
- No existing implementation found
- Related patterns discovered: [list file paths if any]
- Ready to proceed

🔄 **Partially Implemented**
- Found: [what exists with file paths]
- Missing: [what still needs to be done]
- Recommend: [approach to complete]

❌ **Fully Implemented**
- Evidence: [file paths and functionality description]
- Recommend: Close or repurpose JIRA issue

⚠️ **Conflicts Detected**
- Issue: [architectural concerns or blocking problems]
- Recommend: Discuss with team before proceeding

---

## ⛔ STOP - Decision Point

Based on the feasibility analysis above, decide next steps:

**If ready to proceed:**

Standard workflow:
```
/devflow:plan-work $ARGUMENTS
```

**OR** with Test-Driven Development:
```
/devflow:plan-work --tdd $ARGUMENTS
```

TDD mode will:
- Detect test framework and existing test patterns
- Map tests to components being modified
- Generate test cases from acceptance criteria
- Guide RED/GREEN/REFACTOR implementation workflow

**If partially done or conflicts exist:**
Discuss approach with team first

**If fully implemented:**
Close or update JIRA issue

---

⏸️ **Stopped** - Choose your next step above and run the appropriate command
