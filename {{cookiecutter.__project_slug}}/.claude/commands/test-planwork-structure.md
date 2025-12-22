---
description: Test plan-work structure locally
argument-hint: "[--tdd] [ISSUE-KEY]"
allowed-tools: ["Grep", "Glob", "Read", "EnterPlanMode"]
---

# Test Plan Work Structure

Simulating the actual plan-work command structure.

Issue: TEST-123

[Call `EnterPlanMode`]

Now in Plan Mode - I'll fetch the issue and create a detailed plan.

---

## Step 1: Mock JIRA Fetch

Issue: TEST-123 - Add testing section to README
Type: Feature

---

## Step 2: Analyze Codebase & Create Implementation Plan

### Analyze Codebase

[Read README.md to understand structure]

**Findings:**
- File has sections for Setup, Usage, License
- No Testing section exists
- Should insert between Usage and License

### Implementation Plan

**For Features:**
- Create new "## Testing" section
- Add instructions for running tests
- Document test command

**Files to Modify:**
- README.md (line ~280, insert new section)

**Implementation Order:**

1. Add Testing Section
   - Insert at line 280
   - Include pytest command
   - Include coverage instructions

**Note:** Simple documentation addition, no code changes required.

[Call `ExitPlanMode`]

---

## After Plan Approval

[Once ExitPlanMode returns with user approval]:

✅ **Plan approved and saved to plan file.**

**Next Steps:**

To implement this plan, run: `/devflow:implement`

To revise the plan, provide your feedback and I'll update it.

**IMPORTANT:** Do NOT proceed with implementation. The `/devflow:implement` command handles branch creation, JIRA updates, and code changes.
