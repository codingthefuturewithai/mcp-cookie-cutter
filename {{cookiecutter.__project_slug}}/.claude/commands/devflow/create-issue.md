---
description: Create JIRA Executable Spec or Bug issue with codebase analysis
argument-hint: "[brief-description]"
allowed-tools: ["Read", "Grep", "Glob", "mcp__atlassian__getAccessibleAtlassianResources", "mcp__atlassian__getVisibleJiraProjects", "mcp__atlassian__getJiraProjectIssueTypesMetadata", "mcp__atlassian__createJiraIssue", "mcp__context7__resolve-library-id", "mcp__context7__get-library-docs"]
---

# Create JIRA Issue

I'll create a detailed JIRA issue (Executable Spec or Bug) with codebase analysis and Context7 research.

Request: $ARGUMENTS

**Reference docs:** See `reference/FEATURE-EXAMPLE.md`, `reference/BUG-EXAMPLE.md`, `reference/REFERENCE.md`

---

## Step 1: Gather Information

**🚨 CRITICAL: Ask ONE question at a time. Wait for user response before next question.**

**🚨 CRITICAL: MCP handles authentication - NEVER ask for URL/cloudId/credentials!**

---

**Get Atlassian Connection:**

[Call `mcp__atlassian__getAccessibleAtlassianResources` - authentication handled by MCP]

[Extract cloudId from response - user has single instance]

Say: "Connected to Atlassian"

---

**Get Project:**

[Call `mcp__atlassian__getVisibleJiraProjects`]

Ask ONLY: "Which project?" [Display: KEY - Name]

**WAIT.** Store projectKey.

---

**Issue Type:**

Ask ONLY: "What type of issue?"

Options:
1. Feature (new functionality)
2. Bug (something broken)
3. Documentation (docs update)
4. Chore (housekeeping, maintenance)
5. Research (investigation, spike)
6. Technical Debt (refactoring, cleanup)

**WAIT.**

[Map to JIRA types]:
- Feature → "Executable Spec"
- Bug → "Bug"
- Documentation/Chore/Research/Tech Debt → "Task" (will add specific label later)

[Call `mcp__atlassian__getJiraProjectIssueTypesMetadata` to verify type exists]

---

**Title:**

[Suggest title based on description]

Ask ONLY: "Use this title: '[suggested]' or provide your own?"

**WAIT.** Store title.

---

**Priority:**

Ask ONLY: "Priority? (High/Medium/Low)"

**WAIT.** Default Medium if unclear.

---

## Step 2: Analyze Codebase

[Use Grep/Glob/Read to find]:
- **Existing libraries/tools** (search pyproject.toml, package.json, Cargo.toml, go.mod, etc.)
- **Related components/files** for this feature/bug
- **Existing patterns** (imports, error handling, logging, module structure)
- **Integration points** (where this connects)

Present findings with file paths.

---

## Step 3: Research (If Needed)

[Based on user's description and codebase analysis from Step 2]:

**If feature requires library/tool NOT in codebase:**

Say: "This feature needs [library X]. I don't see it in the project. Research options with Context7?"

Ask ONLY: "Yes or No?"

**WAIT.**

**If Yes:**
- `mcp__context7__resolve-library-id`
- `mcp__context7__get-library-docs`

Summarize strategic insights (which library, why, trade-offs) - NOT API docs.

**If feature uses existing libraries:**
- Skip research
- Use existing patterns from codebase

---

## Step 4: Draft Issue

**🎯 CRITICAL - See reference/REFERENCE.md § "Outcomes vs Implementation"**

**Core principle:** WHAT (outcomes, capabilities), not HOW (implementation).

**For Executable Spec:**

**Background & Goal:** Why needed, what achieved

**Acceptance Criteria (3-5 items):**
- ✅ Capabilities, behaviors, data requirements
- ✅ API endpoints, CLI flags, config fields
- ❌ NOT source files, function calls, classes
- Format: Bold titles with sub-bullets
- Testable from user perspective

**Technical Guidance:**
- Version requirements, standards
- **SUGGEST** libraries with rationale
  - ✅ "Consider X for Y"
  - ❌ "Use X.function() in file.py"
- Context7: Strategic (which lib, why), NOT API docs
- Config/template files needed
- Cross-platform notes

**Testing Requirements:** What to test, scenarios, platforms

**For Bug:**

- Problem Statement
- Environment
- Steps to Reproduce
- Current vs Expected
- Root Cause (if known from logs)
- Investigation Areas (components, not exact fixes)
- Potential Approaches (directions, not line-by-line)
- Testing Requirements

**For Documentation:**

- **What needs documenting:** Feature, API, workflow that lacks documentation
- **Current state:** What exists now (outdated, missing, unclear)
- **Desired outcome:** What users should understand after reading
- **Scope:** Which files/sections need updates
- **Accuracy verification:** How to ensure docs match actual behavior
- **Examples needed:** Code samples, use cases, diagrams

**For Chore/Housekeeping:**

- **Maintenance need:** What requires cleanup/updating
- **Current problem:** Why this maintenance is needed (tech debt, outdated dependencies, etc.)
- **Desired outcome:** What improves after completion
- **Impact:** What breaks if not done, what improves when done
- **Scope:** Files, configs, dependencies affected

**For Research:**

- **Questions to answer:** What needs investigation
- **Context:** Why this research is needed now
- **Deliverables:** What format (spike report, proof-of-concept, recommendation)
- **Success criteria:** What decisions can be made after research
- **Time box:** Recommended investigation limit

**For Technical Debt:**

- **Problem being solved:** What technical issue this addresses
- **Current impact:** How this debt affects development/performance
- **Desired outcome:** What improves (code quality, maintainability, performance)
- **Benefit:** Why prioritize this now
- **Scope:** Components affected

---

## Step 5: Labels

[Extract from description + analysis]

Say: "Suggested: `[label1]`, `[label2]`, `[label3]`"

Ask ONLY: "Use these or edit/add?"

**WAIT.** Store labels.

---

## Step 6: Review & Approve

Show complete preview:
- Instance: [name]
- Project: [KEY - Name]
- Type: [Executable Spec or Bug]
- Title: [title]
- Priority: [priority]
- Labels: [labels]
- Full description: [complete text]

Ask ONLY: "Create this JIRA issue?"

Options: "Yes / Edit / Cancel"

**⏸️ WAIT for explicit "Yes"**

- Edit: Ask changes, revise, show again
- Cancel: Stop
- Yes: Proceed

---

## Step 7: Create

[Only if approved]

[Call `mcp__atlassian__createJiraIssue`]

Return: Issue key, URL, suggested branch name.

---

## Rules

**Never:**
- Create without approval
- Use "Story" (must be "Executable Spec")
- Skip codebase analysis
- Ask ONE question at a time

**Always:**
- Reference examples (see reference/ directory)
- Wait for responses at each step
- Focus on outcomes, not implementation
