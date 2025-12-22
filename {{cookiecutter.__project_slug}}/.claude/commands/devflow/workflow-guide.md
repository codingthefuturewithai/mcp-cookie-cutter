---
description: DevFlow Workflow Guide
argument-hint: ""
allowed-tools: []
---

# DevFlow Workflow Guide

A streamlined JIRA development workflow broken into focused phases with human-in-the-loop decision points.

---

## Workflow Overview

```
/fetch-issue [KEY]  →  /plan-work [KEY]  →  /implement  →  /security-review [KEY]  →  /complete [KEY]  →  /post-merge
     ↓                      ↓                    ↓                    ↓                      ↓                ↓
  Fetch &              Branch +            Execute           Security              PR + JIRA         Cleanup
  Analyze              Plan Mode           Plan              Scan                  Done              & Sync
                                                          (Recommended)
```

---

## The Commands

### 1. `/devflow:fetch-issue [ISSUE-KEY]`

**Purpose:** Fetch JIRA issue and analyze feasibility

**What it does:**
- Retrieves issue from JIRA (type, summary, requirements)
- Searches codebase for existing implementations
- Assesses: Not implemented / Partially done / Fully done / Conflicts

**Stops at:** Decision point - proceed, discuss, or close issue

**Next:** `/devflow:plan-work [ISSUE-KEY]` if ready to proceed

---

### 2. `/devflow:plan-work [ISSUE-KEY]`

**Purpose:** Create branch, update JIRA, develop implementation plan

**What it does:**
- Creates git branch (feature/bugfix/task based on type)
- Updates JIRA to "In Progress"
- Enters Plan Mode for analysis
- Discovers code patterns, test patterns, documentation
- Researches technologies with Context7 (if applicable)
- Creates type-aware plan (features vs bugs vs infrastructure vs docs)

**Stops at:** Plan approval - review before implementation

**Next:** `/devflow:implement` after approving plan

---

### 3. `/devflow:implement`

**Purpose:** Execute approved plan with validation

**What it does:**
- Implements changes following discovered patterns
- Tests each component incrementally
- Updates documentation (Definition of Done)
- Commits after each validated logical unit
- Auto re-plans if major deviation needed

**Stops at:** Implementation complete, ready for security review (recommended)

**Next:** `/devflow:security-review [ISSUE-KEY]` (recommended) or `/devflow:complete [ISSUE-KEY]`

---

### 4. `/devflow:security-review [ISSUE-KEY]` (Recommended)

**Purpose:** Analyze code changes for security vulnerabilities

**What it does:**
- Analyzes all files modified on the current branch
- Invokes security-scanner agent for comprehensive analysis
- Checks for OWASP Top 10 vulnerabilities
- Identifies unsafe patterns and provides remediation guidance
- Reports findings by severity (CRITICAL, HIGH, MEDIUM, LOW)

**When to use:**
- **Always recommended** before creating PR
- **Especially important** for:
  - Authentication/authorization logic
  - Input validation or API integrations
  - Database queries or file operations
  - Cryptographic functions or dependencies

**Can also run standalone:**
- `/devflow:security-review` (interactive mode: full repo, specific files, or directory)
- Useful for baseline scans, legacy code review, or targeted analysis

**Stops at:** Security assessment complete, vulnerabilities identified (if any)

**Next:**
- If issues found: Fix vulnerabilities, then re-run security-review
- If clean: `/devflow:complete [ISSUE-KEY]`

---

### 5. `/devflow:complete [ISSUE-KEY]`

**Purpose:** Final validation, create PR, mark JIRA done

**What it does:**
- Runs final validation (adapts to work type)
- Analyzes changes for PR description
- Creates PR with auto-generated description
- Updates JIRA to "Done"

**Stops at:** PR created, waiting for review/merge

**Next:** After PR is merged → `/devflow:post-merge`

---

### 6. `/devflow:post-merge`

**Purpose:** Sync with remote and clean up

**What it does:**
- Switches to main branch
- Pulls merged changes
- Deletes feature branch
- Optionally updates dependencies and runs tests

**Stops at:** Ready for next issue

**Next:** Start new issue with `/devflow:fetch-issue [NEW-KEY]`

---

## Key Design Principles

**Generic & Pattern-Driven**
- Commands work across project types (Python, JavaScript, Go, etc.)
- Discover project-specific patterns instead of prescribing
- Adapt validation strategy to work type

**Type-Aware Planning**
- Features: Components, integration, testing
- Bugs: Reproduction, root cause, regression tests
- Infrastructure: Validation, impact assessment
- Documentation: Accuracy, examples, links

**Human-in-the-Loop**
- Decision boundaries at critical points
- No auto-proceed past approval gates
- User controls workflow progression

**Definition of Done**
- Mandatory test pattern compliance
- Mandatory code pattern compliance
- Mandatory documentation updates

---

## Quick Start

```bash
# 1. Fetch issue and analyze
/devflow:fetch-issue ACT-123

# 2. Create branch and plan (after feasibility check)
/devflow:plan-work ACT-123

# 3. Execute plan (after plan approval)
/devflow:implement

# 4. Security review (recommended, especially for sensitive changes)
/devflow:security-review ACT-123

# 5. Finalize (after security review or if skipped)
/devflow:complete ACT-123

# 6. Cleanup (after PR merged)
/devflow:post-merge
```

---

## Decision Points

**After Fetch:**
- ✅ Not implemented → Continue to planning
- 🔄 Partially implemented → Review and continue
- ❌ Fully implemented → Close issue
- ⚠️ Conflicts → Discuss with team

**After Planning:**
- ✅ Approve → Proceed to implement
- 📝 Revise → Request changes, review again
- ❌ Reject → Discuss alternative

**After Implementation:**
- ✅ Validated → Run security review (recommended)
- ❌ Failed validation → Fix and re-validate
- 🔄 Major deviation → Auto re-plan with approval

**After Security Review:**
- ✅ No issues → Continue to complete
- ⚠️ Issues found → Fix vulnerabilities, re-run security-review
- ⏭️ Can skip if low-risk (docs only, etc.)

**After Complete:**
- Wait for PR review and merge
- Address feedback if needed
- Run post-merge after merge completes

---

## Benefits

**Reduced Cognitive Load:** Each command has one clear purpose

**Natural Flow:** Commands align with how development actually works

**Flexibility:** Can restart at any phase, skip when appropriate

**Quality:** Pattern discovery ensures consistency with existing codebase

**Reusability:** 90% applicable across different project types

---

## Tips

- Each command preserves context for the next step
- Commands discover patterns - don't fight them
- Git branch naming adapts to issue type (feature/bugfix/task)
- Incremental commits keep changes trackable
- Documentation updates are mandatory, not optional
- Test pattern compliance is enforced, not suggested
