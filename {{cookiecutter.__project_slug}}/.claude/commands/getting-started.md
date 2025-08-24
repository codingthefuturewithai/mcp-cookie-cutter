---
description: Interactive guided tour of your MCP server - three paths based on your experience level
argument-hint: ""
allowed-tools: ["Read", "Grep", "Glob", "LS", "Bash", "KillBash", "BashOutput"]
---

# Welcome to Your MCP Server! 

First, let me understand what project we're working with:
```bash
pwd  # Check current directory
# List files (cross-platform)
python -c "import os; [print(f) for f in os.listdir('.')]"
```

Now I can see we're in the [project_name] MCP server with example tools, decorators, and monitoring. Let's get you started!

## 🚨 CRITICAL: Virtual Environment Already Set Up

**DO NOT reinstall dependencies or create a new virtual environment!**
- ✅ Virtual environment exists at `.venv/`
- ✅ All dependencies already installed via `pip install -e .`
- ✅ Server and tools ready to run immediately
- ⚠️ NEVER use global pip - always use `uv run` commands

## Choose Your Path

**What would you like to do?**

1. **Learn MCP basics** - I'll explain what MCP is and how it works
2. **Learn this server** - I know MCP, but how does THIS server work?
3. **Just build** - Skip the talk, let's create a tool

**Type 1, 2, or 3** (you can always ask for help along the way)


## Note for AI Assistants - CRITICAL INSTRUCTIONS

### PATH SELECTION

Based on user's choice (1, 2, or 3), follow the appropriate path:

#### Path 1: Learn MCP Basics
1. Read `.reference/mcp-beginners-guide.md` FIRST
2. Explain MCP concepts ONE at a time (keep each brief - 2-3 sentences):
   
   **Concept**: What MCP is (AI with tools)
   - "MCP lets AI assistants use tools to DO things, not just talk"
   - Example: fetch data, run calculations, control apps
   - "Does this make sense?"
   [WAIT FOR USER RESPONSE BEFORE CONTINUING]
   
   **Concept**: Server vs Client architecture
   - "MCP has servers (provide tools) and clients (use tools)"
   - "YOUR code is a server. Claude/Cursor are clients"
   - "Think: your server serves tools to AI assistants"
   - "Clear so far?"
   [WAIT FOR USER RESPONSE BEFORE CONTINUING]
   
   **Concept**: How MCP connects
   - "Three transport methods:"
   - "• STDIO (local) - what Claude Desktop uses"
   - "• SSE (network) - traditional HTTP transport"
   - "• Streamable HTTP - modern unified transport with session management"
   - "This server supports all three transports. FastMCP handles the complexity."
   - "Making sense?"
   [WAIT FOR USER RESPONSE BEFORE CONTINUING]
   
   **Concept**: What tools are (Python functions)
   - "Tools are just async Python functions that DO things - fetch data OR take actions"
   - Show examples:
   ```python
   # Tool that FETCHES data
   async def get_weather(city: str) -> dict:
       # Fetch weather data
       return {"city": city, "temp": 72, "conditions": "sunny"}
   
   # Tool that TAKES ACTION
   async def create_file(filename: str, content: str) -> dict:
       # Actually creates a file on disk
       with open(filename, 'w') as f:
           f.write(content)
       return {"status": "success", "file": filename}
   ```
   - "The server exposes these so AI assistants can both gather info AND perform tasks"
   - "Any questions about the code?"
   [WAIT FOR USER RESPONSE BEFORE CONTINUING]
3. After MCP basics: "Now let me explain what makes THIS server unique..."
4. **CONTINUE TO DECORATOR CONCEPTS SECTION BELOW**

### DECORATOR CONCEPTS (Used by both Path 1 and Path 2)

**Concept**: Our Unique Decorator Pattern
- "Most MCP servers use @mcp.tool on each function"
- "This server is DIFFERENT - let me show you..."
- Show ACTUAL app.py code snippet:
```python
# Standard MCP servers do this:
@mcp.tool
async def my_tool(): ...

# WE do this (in app.py):
for func in [tool1, tool2]:
    decorated = exception_handler(func)
    decorated = tool_logger(decorated) 
    decorated = type_converter(decorated)
    app.tool()(decorated)
```
- "Does this pattern make sense? Questions?"
[WAIT FOR USER RESPONSE BEFORE CONTINUING]

**Concept**: The 5 Decorators & What They Do
- "Your tools get these superpowers automatically:"
- "🛡️ exception_handler - Catches crashes, clean error messages"
- "📊 tool_logger - Logs every execution with timing"
- "🔄 type_converter - MCP sends strings, your tools get proper types"
- "💾 sqlite_logger - Permanent database record"
- "⚡ parallelize - Process lists across multiple workers"
- "Clear on what each does?"
[WAIT FOR USER RESPONSE BEFORE CONTINUING]

**Concept**: How to Add YOUR Tools
- "Look at the bottom of tools/example_tools.py - two lists:"
```python
# List of regular example tools
example_tools = [
    echo_tool,
    get_time,
    # ← You'll add YOUR tools to similar lists
]

# List of tools that benefit from parallelization
parallel_example_tools = [
    process_batch_data,
    # ← Or here for parallel processing
]
```
- "For YOUR tools:"
- "Step 1: Write tool in tools/your_tools.py"
- "Step 2: Create similar lists in YOUR file"
- "Step 3: Import in {{cookiecutter.__project_slug}}/server/app.py using your project name (check directory name)"
- "That's it! Decorators applied automatically"
- "Make sense?"
[WAIT FOR USER RESPONSE BEFORE CONTINUING]

**Concept**: When to Use Parallel
- "Use example_tools (standard) for:"
- "• Quick operations (<1 second)"
- "• Database queries, API calls"
- "• Single item processing"
- ""
- "Use parallel_example_tools for:"
- "• Processing lists of items"
- "• Heavy computations (>1 second each)"
- "• Batch operations"
- ""
- "Simple rule: Lists → parallel, Single → standard"
- "Questions about when to use which?"
[WAIT FOR USER RESPONSE BEFORE CONTINUING]

### AFTER DECORATOR CONCEPTS
- "Want to test a real tool?" → Inspector demo
- **EXIT**: Kill all processes, then "Ready to build your own?"

#### Path 2: Learn This Server  
**LANGUAGE**: Use "I'll explain", "Let me show you", "I'll help you understand"

1. Read `.reference/patterns/tool_patterns.py` FIRST
2. Say: "I'll explain what makes YOUR server DIFFERENT from other MCP servers..."
3. **GO TO DECORATOR CONCEPTS SECTION ABOVE** - Present each concept with stops
4. After decorator concepts, continue here:
   ```bash
   # Show tools directory (cross-platform)
   python -c "import os; print('Tools:', os.listdir('tools'))"
   ```
5. **MENTION (don't launch) the UI**:
   ```
   "You also have an admin dashboard at streamlit run {{cookiecutter.__project_slug}}/ui/app.py
   (We can explore that later if you want)"
   ```
6. **CONTINUE TO AFTER DECORATOR CONCEPTS SECTION**

#### Path 3: Just Build
1. Quick warning: "⚠️ Note: This server uses a unique decorator pattern - check tools/example_tools.py to see how tools are organized"
2. Immediately transition: "Let's build a tool. Use `/add-tool` command"
3. No other explanations unless they ask

### PROCESS MANAGEMENT - CRITICAL

**Check for running processes BEFORE any operation**:
```bash
# Windows PowerShell:
Get-Process | Where-Object {$_.ProcessName -match "python|uv"} | Select-Object Id, ProcessName
# Mac/Linux:
ps aux | grep -E "mcp|uv run" | grep -v grep
```

**Kill processes when**:
- Exiting Inspector testing
- Before modifying tools
- Before generating tests
- Switching between activities

**Kill ONLY project processes**:
```bash
# Windows:
taskkill /PID <PID> /F  # Only PIDs from THIS project
# Mac/Linux:
kill <PID>  # Only PIDs from THIS project
```

**Explain why**: "Killing Inspector/server because tools changed - need fresh start"

### INSPECTOR INSTRUCTIONS

**⚠️ CRITICAL: CLOSE ALL OLD BROWSER TABS FIRST! ⚠️**
```
🚨 BEFORE STARTING INSPECTOR:
   Close ANY existing MCP Inspector tabs in ALL browsers!
   Old tabs cause "Error Connecting to MCP Inspector Proxy"
   Check Chrome, Firefox, Safari, Arc, etc.
```

**For ALL users testing tools**:
1. Start: `uv run mcp dev {{cookiecutter.__project_slug}}/server/app.py`
2. "Inspector at http://localhost:6274"
3. "Click Connect button on LEFT side!"
4. "Click Tools tab → List Tools"
5. "Select your tool and click 'Run Tool'"

**After testing**: 
- "Done testing? CLOSE the browser tab first!"
- "Then let me kill the processes before we continue"

### DEBUG SUPPORT

**When user tests and it fails**:
1. "What happened? Share the error"
2. "Check browser console (F12) for details"
3. "Copy error or take screenshot"
4. Guide through specific fix
5. "Let's restart and try again"

### HELP AT ANY TIME

**User can always say**:
- "I don't understand" → Explain current concept
- "What just happened?" → Clarify last action
- "Show me again" → Repeat demonstration
- "I need help" → Offer debug assistance

### TRANSITION POINTS

**Path 1 → Building**: "Now that you understand MCP, ready to build?"
**Path 2 → Building**: "Now that you know your server, ready to add tools?"
**Path 3**: Already building

**ALL paths converge to**: `/add-tool` command

### REMEMBER

- **ENVIRONMENT IS READY** - .venv exists with all dependencies installed
- **NEVER use pip install** - Environment already complete
- **ALWAYS use `uv run`** - For all Python/pytest commands
- **NEVER use global Python** - Always use the project's .venv via uv
- **ALWAYS check processes** - Before operations
- **ONE concept at a time** - For learners
- **Debug support always** - For everyone