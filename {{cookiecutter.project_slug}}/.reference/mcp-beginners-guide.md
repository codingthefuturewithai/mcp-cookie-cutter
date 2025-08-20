# MCP Beginners Guide

## What is MCP?

MCP (Model Context Protocol) is a protocol that lets AI assistants like Claude actually DO things, not just talk about them. Think of it as giving AI assistants "hands" to interact with the world.

### Without MCP:
- User: "What's the weather?"
- AI: "I can't check the weather, but you can visit weather.com"

### With MCP:
- User: "What's the weather?"
- AI: *Actually fetches weather data* "It's 72°F and sunny in San Francisco"

## Core Concepts

### 1. Tools
Tools are Python functions that DO things:
- Fetch data from APIs
- Read/write files
- Query databases
- Control applications
- Perform calculations

### 2. Server vs Client Architecture

**MCP Server** (what you're building):
- Provides tools
- Handles tool execution
- Returns results

**MCP Client** (Claude, Cursor, etc.):
- Discovers available tools
- Calls tools when needed
- Receives results

Think of it like a restaurant:
- Server (kitchen) = Your MCP server with tools
- Client (waiter) = Claude taking orders and delivering results
- User (customer) = The person asking for things

### 3. Transport Methods

How clients connect to servers:

**STDIO (Standard I/O)**:
- Local connection
- Used by Claude Desktop
- Fast and secure
- No network needed

**SSE (Server-Sent Events)**:
- Network connection
- Traditional HTTP
- Good for web clients

**Streamable HTTP**:
- Modern network connection
- Supports sessions
- Better error handling

## How MCP Works

1. **Client connects** to your server
2. **Client discovers** available tools
3. **User makes request** that needs a tool
4. **Client calls tool** on your server
5. **Server executes** the tool
6. **Server returns** results
7. **Client uses results** in response

## Example Flow

User: "Create a file called notes.txt with my meeting agenda"

1. Claude recognizes this needs a file creation tool
2. Claude calls your `create_file` tool with:
   - filename: "notes.txt"
   - content: "Meeting Agenda\n1. Project updates\n2. Next steps"
3. Your server creates the file
4. Your server returns: {"status": "success", "path": "/Users/you/notes.txt"}
5. Claude tells user: "I've created notes.txt with your meeting agenda"

## Your First Tool

Here's a complete, working MCP tool:

```python
async def get_time(
    timezone: str = "UTC",
    format: str = "24h"
) -> Dict[str, Any]:
    """Get the current time in any timezone.
    
    Args:
        timezone: Timezone name (e.g., 'America/New_York')
        format: Time format ('24h' or '12h')
    
    Returns:
        Dictionary with time information
    """
    from datetime import datetime
    import pytz
    
    tz = pytz.timezone(timezone)
    now = datetime.now(tz)
    
    if format == "12h":
        time_str = now.strftime("%I:%M %p")
    else:
        time_str = now.strftime("%H:%M")
    
    return {
        "time": time_str,
        "timezone": timezone,
        "date": now.strftime("%Y-%m-%d"),
        "day": now.strftime("%A")
    }
```

## Key Points for Beginners

1. **Tools are just functions** - If you can write a Python function, you can write an MCP tool

2. **Async is required** - All tools must be `async def`, not just `def`

3. **Type hints are mandatory** - MCP needs to know what types your parameters are

4. **Return dictionaries** - Tools should return structured data as dicts

5. **Handle errors gracefully** - Don't let exceptions crash the server

6. **Think "actions"** - Tools should DO things or FETCH things

## Common Beginner Mistakes

### Mistake 1: Using Optional Types
```python
# ❌ WRONG - Optional breaks MCP
async def my_tool(text: Optional[str] = None):
    ...

# ✅ RIGHT - Use concrete defaults
async def my_tool(text: str = ""):
    ...
```

### Mistake 2: Forgetting Async
```python
# ❌ WRONG - Must be async
def my_tool(text: str):
    ...

# ✅ RIGHT - Always async
async def my_tool(text: str):
    ...
```

### Mistake 3: No Type Hints
```python
# ❌ WRONG - MCP needs types
async def my_tool(text):
    ...

# ✅ RIGHT - Always include types
async def my_tool(text: str) -> Dict[str, Any]:
    ...
```

## What Makes This Server Special

This MCP server template includes powerful decorators that automatically enhance your tools:

1. **Exception Handler**: Catches errors and returns clean messages
2. **Tool Logger**: Logs every execution with timing
3. **Type Converter**: Converts string parameters to correct types
4. **Parallelize**: Runs batch operations across multiple workers

You don't need to understand these yet - they work automatically!

## Next Steps

1. **Explore the example tools** in `tools/example_tools.py`
2. **Test with MCP Inspector** at http://localhost:6274
3. **Create your first tool** using the `/add-tool` command
4. **Connect to Claude Desktop** when ready

Remember: MCP is just a way for AI to run Python functions. If you can write Python, you can build MCP tools!