---
description: Test the plan-work flow structure locally
allowed-tools: ["Read", "EnterPlanMode"]
---

# Test DevFlow Plan Work Flow

Testing the plan-work flow in this cookiecutter project.

Issue: TEST-001 - Add usage examples to main README

[Call `EnterPlanMode`]

Now in Plan Mode - I'll create a simple plan.

---

## Step 1: Analyze Repository

[Read README.md from the cookiecutter root]

**Repository analyzed**

---

## Step 2: Create Simple Plan

**Objective:** Add usage examples section to README

**Changes needed:**
- Add "Usage Examples" section
- Include 2-3 common scenarios
- Add code snippets

**Files to modify:**
- README.md

**Validation:**
- Verify examples are accurate
- Test code snippets work

[Call `ExitPlanMode`]

---

## After Plan Approval

[Once ExitPlanMode returns with user approval]:

✅ **Plan approved and saved to plan file.**

**Next Steps:**

To implement this plan, run: `/devflow:implement`

To revise the plan, provide your feedback and I'll update it.

**IMPORTANT:** Do NOT proceed with implementation. The `/devflow:implement` command handles branch creation, JIRA updates, and code changes.
