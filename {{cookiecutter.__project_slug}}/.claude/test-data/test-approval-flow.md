---
description: Test approval flow with conditional branches
allowed-tools: ["Read", "EnterPlanMode"]
---

# Test Approval Flow

Testing if conditional branches work in slash commands.

---

[Call `EnterPlanMode`]

Now in plan mode. Let me read a file:

[Read README.md]

Plan created: Add a "Testing" section to README.

---

**Do you approve this plan?**

- If **YES**: I'll provide next steps
- If **NO**: Tell me what to change
- To **CANCEL**: Say "cancel"

[WAIT for user response - do NOT continue]

[If user approves]:

---

✅ **Plan approved**

**Next steps:**

Run `/devflow:implement`

---

[Then END naturally - do not call ExitPlanMode, do not continue, just stop]

[If user wants changes]:

Tell me what to revise.
