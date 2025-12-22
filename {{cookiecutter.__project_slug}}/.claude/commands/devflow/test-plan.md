---
description: Simple test to verify plan-work flow
allowed-tools: ["Read", "EnterPlanMode"]
---

# Test Plan Work Flow

**This is a test command to verify the plan-work flow works correctly.**

Issue: TEST-001 - Add FAQ section to README

[Call `EnterPlanMode`]

Now in Plan Mode - I'll analyze the README and create a simple plan.

---

## Step 1: Analyze Current README

[Read README.md to see current structure]

**Current sections identified**

---

## Step 2: Create Simple Implementation Plan

**Objective:** Add a FAQ section after the existing content

**Implementation Steps:**

1. Add new "## FAQ" section
2. Include 3-5 common questions
3. Maintain existing formatting style

**Files to modify:**
- README.md (add FAQ section at end)

**Validation:**
- Verify markdown formatting
- Check links work
- Ensure no existing sections disrupted

[Call `ExitPlanMode`]

---

## After Plan Approval

[Once ExitPlanMode returns with user approval]:

✅ **Plan approved and saved to plan file.**

**Next Steps:**

To implement this plan, run: `/devflow:implement`

To revise the plan, provide your feedback and I'll update it.

**IMPORTANT:** Do NOT proceed with implementation. The `/devflow:implement` command handles branch creation, JIRA updates, and code changes.
