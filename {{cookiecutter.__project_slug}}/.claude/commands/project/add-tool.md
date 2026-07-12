---
description: Design and implement a new MCP tool - planning first, then implementation with your approval
argument-hint: "[brief-description-of-tool]"
allowed-tools: ["Read", "Write", "Edit", "Grep", "Glob", "Bash", "KillBash"]
---

# Creating Your New MCP Tool

First, let me check the project structure:
```bash
pwd
# List tools directory (cross-platform)
python -c "import os; [print(f) for f in os.listdir('tools')]"
```

## 🚨 IMPORTANT: Environment Ready

**Virtual environment and dependencies already installed!**
- ✅ No need to create venv or install packages
- ✅ Use `uv run` for all commands
- ⚠️ NEVER use global pip

## CRITICAL: Process Check First

Let me check if any MCP processes are running that need to be killed:

```bash
# First, determine our project name
pwd
# Then check for processes related to THIS project
# Windows PowerShell:
Get-Process | Where-Object {$_.ProcessName -match "python|uv"} | Select-Object Id, ProcessName
# Mac/Linux:
ps aux | grep -E "mcp|uv run" | grep -v grep
```

If processes found for this project: "I need to kill these processes before we modify tools"

## Step 0: MANDATORY - Read Compatibility Rules

**🚨 STOP! READ THIS FIRST:**
```bash
cat .reference/mcp-compatibility-critical.md
```

**KEY RULE: Prefer concrete defaults over Optional[...] parameters.**
- ✅ PREFER: concrete types with defaults: `[]`, `0`, `""`, `False`
- ⚠️ Optional[...] works on modern MCP clients (SDK 1.28+ validates via
  Pydantic), but concrete defaults keep schemas simpler and maximally
  compatible - see .reference/mcp-compatibility-critical.md

## Step 1: MANDATORY - Check for Context7 Research Tool

**I MUST check if context7 is available:**

Try to use context7 to test availability:
```
Attempting: context7 - resolve-library-id (MCP)(libraryName: "test")
```

### If context7 WORKS:
- ✅ Continue to Step 2

### If context7 FAILS or is NOT FOUND:
```
⚠️ IMPORTANT: You don't have context7 configured!
This tool provides efficient library documentation lookup.
Without it, research may be outdated or inaccurate.

To add context7, run this in your terminal:
claude mcp add-json -s user context7 '{"type":"stdio","command":"npx","args":["-y","@upstash/context7-mcp@latest"]}'

Then restart Claude Code with: claude --resume

Do you want to:
1. Install context7 first (recommended)
2. Continue with WebSearch only (less accurate)
3. Cancel and come back later

Please choose (1, 2, or 3):
```

## 🛑 STOP HERE IF NO CONTEXT7

**WAIT for user's choice before continuing**
- If user chooses 1: Stop and wait for them to install
- If user chooses 2: Continue with WebSearch only
- If user chooses 3: Exit the command

**DO NOT SKIP THIS CHECK**

## Step 2: Understanding Your Request

Based on what you want: "$ARGUMENTS"

I'll analyze what libraries and frameworks this will need.

## Step 3: MANDATORY Library Research

**CRITICAL**: I MUST research all libraries/frameworks before planning.

**Researching these components:**
- [List each library/framework/API the tool will use]
- [Use context7 if available, else WebSearch]
- [Check latest versions and API changes]

```
📚 Research Results:
- Library X: Latest version Y.Z, API docs reviewed
- Framework A: Version B.C recommended, breaking changes noted
- Tool D: Current best practices confirmed
```

## Step 4: Tool Design Plan (Based on Research)

**IMPORTANT**: This plan is based on current documentation, not training data.

**🚨 CRITICAL: Read MCP Compatibility Rules**
```
Reading .reference/mcp-compatibility-critical.md for MANDATORY compatibility rules...

KEY RULE: Prefer concrete defaults over Optional[...] types (convention):
- Use empty string defaults instead of Optional[str]
- Use 0 or -1 instead of Optional[int]
- Use empty list [] instead of Optional[List]
(Optional works on modern clients; concrete defaults maximize compatibility)
```

Based on your requirements AND my research, here's what I'll create:

### Tool Overview
- **Name**: [tool_name]
- **Purpose**: [what it does]
- **Parameters**: [list with types AND defaults - prefer concrete defaults over Optional]
- **Returns**: [specific return type and structure]

### Technical Implementation

**Dependencies & Versions:**
- [library]==X.Y.Z - [what it's for]
- [other libs with versions] - [purpose]

**Implementation Approach:**
- Async pattern: [how async will be handled]
- Error handling: [specific strategy, fallbacks]
- Data structure: [exact dict/list structure returned]

**External Services/Auth:** 
- None required OR
- [Service name]: [Auth method, e.g., "Token from env var GITHUB_TOKEN"]

**Known Considerations:** [only if relevant]
- API rate limits: [if applicable]
- Resource usage: [if loading large data]
- Platform differences: [if OS-specific]

### Example Usage
```python
# In MCP Inspector
tool_name(param1="value", param2="value")
# Expected output: {...specific example...}
```

**Your Options:**
- ✅ Approve this plan → I'll implement it
- 📝 Request changes → Tell me what to modify
- ❓ Questions → Ask for clarification

**Do you approve this plan?**

## 🛑 STOP HERE - WAIT FOR USER APPROVAL

**DO NOT CONTINUE PAST THIS POINT WITHOUT EXPLICIT USER APPROVAL**

The user must say something like:
- "Yes, proceed"
- "Looks good, implement it"
- "Go ahead"
- "That works"

If the user suggests changes, revise the plan and ask again.

---

## CRITICAL INSTRUCTIONS FOR AI ASSISTANTS

**MANDATORY STOP POINT:**
1. You MUST STOP after presenting the plan
2. You MUST WAIT for explicit user approval
3. NEVER proceed to implementation without user saying "yes" or equivalent
4. If user provides feedback, revise plan and ask again

**MANDATORY COMPATIBILITY REQUIREMENT:**
1. You MUST read .reference/mcp-compatibility-critical.md FIRST
2. Prefer concrete defaults over Optional[...] types (template convention)
3. Use empty defaults instead (empty string, 0, empty list)
4. Test the generated code follows compatibility rules

**MANDATORY RESEARCH REQUIREMENT:**
1. You MUST research EVERY library/framework/API mentioned
2. You MUST use context7 (if available) or WebSearch
3. You MUST show proof of research in your plan
4. You MUST base implementation on current docs, NOT training data
5. NEVER skip research - your training data is ALWAYS outdated

---

## Step 5: Implement the Tool (ONLY AFTER APPROVAL)

**⚠️ This section only executes AFTER user approves the plan above**

**FINAL CHECK - PARAMETER CONVENTIONS:**
Before writing any code, verify:
- ⚠️ Concrete defaults preferred over `Optional[...]` in parameters
- ✅ ALL optional parameters use concrete defaults
- ✅ Example: `directories: List[str] = []` preferred over `Optional[List[str]]`

### Implementation Guidelines
Following the pattern from .reference/patterns/tool_patterns.py:
- Must be an async function
- Must include `ctx: Context = None` as the last parameter
- Must have type hints for all parameters (concrete defaults preferred)
- Must have a comprehensive docstring

Creating the tool in an appropriate module...

## Step 6: Register the Tool

Two registration touchpoints:

1. Add the tool function to the appropriate list in
   `{{cookiecutter.__project_slug}}/tools/example_tools.py` (or your own
   tools module) so `register_tools()` picks it up.
2. Add a `TOOL_METADATA` entry for the tool (same file): a human-readable
   `title` and `ToolAnnotations` behavior hints (`readOnlyHint`,
   `destructiveHint`, `idempotentHint`, `openWorldHint`). Hosts use these
   for permission UX and display. Also consider a typed Pydantic return
   for structured output (see `get_weather`).

Updating {{cookiecutter.__project_slug}}/server/app.py to register the new tool with appropriate decorators:
- For regular tools: @exception_handler → @tool_logger
- For parallel tools: @exception_handler → @tool_logger → @parallelize

## Step 7: Testing Your New Tool in MCP Inspector

**⚠️ CRITICAL: BROWSER TAB CHECK! ⚠️**
```
🚨 BEFORE STARTING INSPECTOR:
   Close ANY existing MCP Inspector tabs (http://localhost:6274)
   in ALL your browsers (Chrome, Firefox, Safari, Arc, etc.)
   Old tabs cause "Error Connecting to MCP Inspector Proxy"
```

Now I'll start the MCP Inspector for you to test:

```bash
# Starting the Inspector
uv run mcp dev {{cookiecutter.__project_slug}}/server/app.py
```

The Inspector is running at http://localhost:6274

**YOUR TURN - Please test the tool:**
1. Open http://localhost:6274 in a **NEW** browser tab
2. Click "Connect" button on the LEFT side
3. Click "Tools" tab → "List Tools"
4. Find your new tool: `[tool_name]`
5. Click it and test with sample inputs
6. Click "Run Tool" to execute

## 🛑 STOP HERE - WAIT FOR USER TO TEST

**I MUST WAIT for you to test the tool and report back**

Tell me one of these:
- "It works" / "Success" → I'll offer to generate tests
- "Error" / "Failed" → Share the error for debugging
- "Done testing" → I'll clean up and we can continue

**DO NOT CONTINUE until the user has tested the tool**

## Step 8: After User Reports Testing Results

**Based on user's response:**

### If "It works" / "Success":
1. Kill the Inspector process
2. Tool creation is complete!

### If "Error" / "Failed":
1. Keep Inspector running for debugging
2. Ask for error details
3. Debug and fix the issue
4. Return to Step 7 for retesting

### If "Done testing":
1. Kill the Inspector process
2. Tool creation is complete!

**Process cleanup:**
```bash
# Find and kill processes
# Windows:
tasklist | findstr /I "python uv"
taskkill /PID <PID> /F
# Mac/Linux:
ps aux | grep -E "mcp|uv run" | grep -v grep
kill <PIDs>
```

## ✅ Tool Creation Complete!

Your new tool has been successfully:
1. Created with comprehensive documentation
2. Registered with decorators (exception handling, logging, type conversion)
3. Tested and verified working in MCP Inspector

**Next Steps:**

### Generate Tests for Your Tool
Now that your tool is working, you should create tests for it:

```
/generate-tests [tool_name]
```

This will create comprehensive unit and integration tests following MCP best practices.

### Or Continue Development
- Add another tool: `/add-tool`
- Remove example tools: `/remove-examples` (clean up the example tools from the codebase)
- Start development server: `mcp dev {{cookiecutter.__project_slug}}/server/app.py`
- Check the UI: `streamlit run {{cookiecutter.__project_slug}}/ui/app.py`