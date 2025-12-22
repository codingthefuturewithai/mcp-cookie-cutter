---
description: Test what happens when we DON'T call ExitPlanMode
allowed-tools: ["Read", "EnterPlanMode"]
---

# Test Plan Exit Behavior

Testing: Does NOT calling ExitPlanMode prevent the implementation prompt?

---

[Call `EnterPlanMode`]

Now in plan mode. I'll do some read-only work.

[Read a simple file to show plan mode is working]

---

## Test Complete

This is the end of the command.

**CRITICAL: I am NOT calling ExitPlanMode.**

Let's see what happens:
- Does Claude Code automatically call ExitPlanMode?
- Does it show the "Would you like to proceed?" prompt?
- Or does it just end cleanly?

---

**Expected Behavior A:** If Claude Code automatically calls ExitPlanMode, we'll see the 3-option prompt.

**Expected Behavior B:** If it doesn't auto-call ExitPlanMode, the command just ends (still in plan mode).

Let's find out...

[I am deliberately NOT calling ExitPlanMode here]
