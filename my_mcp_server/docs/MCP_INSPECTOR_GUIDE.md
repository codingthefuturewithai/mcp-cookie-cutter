# MCP Inspector Testing Guide for My MCP Server

This guide helps you test your MCP server tools using the MCP Inspector, including troubleshooting common setup issues.

## Prerequisites

### 1. Virtual Environment Setup

**CRITICAL**: Always ensure you're using the virtual environment's MCP, not any global installation.

```bash
# From your project root
cd my_mcp_server

# Activate your virtual environment
source .venv/bin/activate  # macOS/Linux
# OR
.venv\Scripts\activate     # Windows

# Verify MCP is using the correct version
which mcp
# Should show: /path/to/my_mcp_server/.venv/bin/mcp
# NOT: /opt/homebrew/bin/mcp or /usr/local/bin/mcp
```

**If you see a global path**, you have two options:

1. Use the full path to your venv's mcp:
   ```bash
   .venv/bin/mcp dev my_mcp_server/server/app.py
   ```

2. Fix your PATH (recommended):
   ```bash
   # Check your PATH order
   echo $PATH | tr ':' '\n' | head -5
   
   # Deactivate and reactivate
   deactivate
   source .venv/bin/activate
   which mcp  # Should now show venv path
   ```

### 2. Install Dependencies

If you haven't already:
```bash
uv sync
```

## Launching MCP Inspector

The MCP Inspector supports multiple transport protocols. Choose the one that best fits your needs:

### STDIO Transport (Default)
From your project root (with venv activated):
```bash
mcp dev my_mcp_server/server/app.py
```

### Default Transport (STDIO)
```bash
mcp dev my_mcp_server/server/app.py
```

### SSE Transport
To test with SSE transport, run the server directly:
```bash
python -m my_mcp_server.server.app --transport sse
```

### Streamable HTTP Transport (Recommended for Testing)
The Streamable HTTP transport provides the best testing experience with its unified endpoint:
```bash
python -m my_mcp_server.server.app --transport streamable-http
```

Note: The `mcp dev` command always uses STDIO transport. To test other transports, run the server directly using the Python module.

You should see:
- Server logs showing tool registration
- SQLite database initialization  
- Inspector URL: http://127.0.0.1:6274

Open the Inspector URL in your browser.

### Transport Comparison

| Transport | Use Case | Endpoint | Features |
|-----------|----------|----------|----------|
| STDIO | Desktop clients (Claude Desktop) | N/A | Simple, reliable |
| SSE | Web clients (legacy) | Multiple endpoints | Separate streams per operation |
| Streamable HTTP | Modern web clients | Single `/mcp` endpoint | Unified API, resumability, better performance |


## Testing Example Tools

### Regular Tools (Form Mode)

These tools work with the standard form interface in MCP Inspector.

#### 1. echo_tool

**Purpose**: Echoes back your input message

**Test Examples**:
```
message: "Hello, MCP!"
Expected: "Echo: Hello, MCP!"

message: "Testing decorators"
Expected: "Echo: Testing decorators"

message: "Hello World"
Expected: "Echo: Hello World"
```

#### 2. get_time

**Purpose**: Returns the current time in human-readable format

**Test Examples**:
```
No parameters required - just click "Run Tool"
Expected: "Current time: YYYY-MM-DD HH:MM:SS"

Example output: "Current time: 2025-01-15 10:30:45"
```

#### 3. random_number

**Purpose**: Generates a random number within a specified range

**Test Examples**:
```
min_value: 1
max_value: 10
Expected: {"number": <1-10>, "range": "1-10", "timestamp": 1234567890.123}

min_value: 100
max_value: 200
Expected: {"number": <100-200>, "range": "100-200", "timestamp": 1234567890.123}

Leave both empty to use defaults (1-100)
Expected: {"number": <1-100>, "range": "1-100", "timestamp": 1234567890.123}
```

#### 4. calculate_fibonacci

**Purpose**: Calculates the nth Fibonacci number

**Test Examples**:
```
n: 5
Expected: {"position": 5, "value": 5, "calculation_time": 0.0000XX}

n: 10
Expected: {"position": 10, "value": 55, "calculation_time": 0.0000XX}

n: 20
Expected: {"position": 20, "value": 6765, "calculation_time": 0.0000XX}
```

### Parallel Tools (JSON Mode Required)

⚠️ **Important**: The parallelization decorator transforms these tools to accept a single parameter `kwargs_list` containing a list of dictionaries. Each dictionary in the list represents one execution of the original function.

**How to Use JSON Mode**:
1. Select the parallel tool
2. Click "Switch to JSON" button
3. Replace the contents with the JSON examples below
4. Click "Run Tool"

#### 5. process_batch_data

**Purpose**: Processes multiple batches of data in parallel

**Decorated Signature**: `process_batch_data(kwargs_list: List[Dict[str, Any]])`

**Original function parameters**:
- `items`: List of strings to process
- `operation`: Operation to perform ('upper', 'lower', 'reverse')

**Test Example 1** - Process three batches with different operations:
```json
{
  "kwargs_list": [
    {"items": ["apple", "banana", "cherry"], "operation": "upper"},
    {"items": ["DOG", "CAT", "BIRD"], "operation": "lower"},
    {"items": ["hello", "world"], "operation": "reverse"}
  ]
}
```

Expected output (list of results for each batch):
```json
[
  {
    "original": ["apple", "banana", "cherry"],
    "processed": ["APPLE", "BANANA", "CHERRY"],
    "operation": "upper",
    "timestamp": 1234567890.123
  },
  {
    "original": ["DOG", "CAT", "BIRD"],
    "processed": ["dog", "cat", "bird"],
    "operation": "lower",
    "timestamp": 1234567890.124
  },
  {
    "original": ["hello", "world"],
    "processed": ["olleh", "dlrow"],
    "operation": "reverse",
    "timestamp": 1234567890.125
  }
]
```

**Test Example 2** - Single batch processing:
```json
{
  "kwargs_list": [
    {"items": ["test", "data"], "operation": "upper"}
  ]
}
```

#### 6. simulate_heavy_computation

**Purpose**: Simulates multiple heavy computation tasks in parallel

**Decorated Signature**: `simulate_heavy_computation(kwargs_list: List[Dict[str, Any]])`

**Original function parameter**:
- `complexity`: Complexity level from 1-10 (default: 5)

**Test Example** - Multiple computations with different complexities:
```json
{
  "kwargs_list": [
    {"complexity": 2},
    {"complexity": 5},
    {"complexity": 8}
  ]
}
```

Expected output (list of results for each computation):
```json
[
  {
    "complexity": 2,
    "iterations": 200000,
    "result": <calculated_value>,
    "computation_time": 0.XXX,
    "operations_per_second": XXXXX.XX
  },
  {
    "complexity": 5,
    "iterations": 500000,
    "result": <calculated_value>,
    "computation_time": 0.XXX,
    "operations_per_second": XXXXX.XX
  },
  {
    "complexity": 8,
    "iterations": 800000,
    "result": <calculated_value>,
    "computation_time": 0.XXX,
    "operations_per_second": XXXXX.XX
  }
]
```


## Testing Error Handling

The decorators provide comprehensive error handling. Test these scenarios:

1. **Invalid input types**:
   - For `calculate_fibonacci`: Try `n: -5` (negative number)
   - For `random_number`: Try `min_value: 100, max_value: 1` (min > max)

2. **Missing required parameters**:
   - Leave required fields empty
   - The error response should clearly indicate what's missing


3. **Invalid parallel tool data**:
   - For `process_batch_data`: Try invalid operation: `{"operation": "invalid"}`
   - For empty arrays: Try `{"batches": []}`


## Viewing Logs

The decorators automatically log all tool executions.

### Log Locations

**Text Logs**:
- macOS: `~/Library/Logs/mcp-servers/my_mcp_server.log`
- Linux: `~/.local/state/mcp-servers/logs/my_mcp_server.log`
- Windows: `%LOCALAPPDATA%\mcp-servers\logs\my_mcp_server.log`

**SQLite Database** (tool execution history):
- macOS: `~/Library/Application Support/my_mcp_server/tool_logs.db`
- Linux: `~/.local/share/my_mcp_server/tool_logs.db`
- Windows: `%LOCALAPPDATA%\my_mcp_server\tool_logs.db`


### Viewing Logs in Admin UI

You can also view logs through the Streamlit admin interface:

```bash
streamlit run my_mcp_server/ui/app.py
```

Navigate to the "Logs" page to see:
- Tool execution history
- Success/failure rates
- Performance metrics
- Detailed error messages


## Common Issues

### ModuleNotFoundError

If you see `ModuleNotFoundError: No module named 'my_mcp_server'`:

1. Ensure you're in the project root directory
2. Check virtual environment is activated: `which python`
3. Reinstall: `uv sync`
4. Use full mcp path: `.venv/bin/mcp dev my_mcp_server/server/app.py`

### MCP Inspector Not Loading

1. Check server started without errors
2. Check if port 6274 is already in use
3. Clear browser cache and refresh

### Tools Not Appearing

1. Check server logs for registration messages
2. Refresh the Inspector page
3. Verify no import errors in terminal

## Next Steps

Once you've verified the example tools work:

1. Add your own tools in `my_mcp_server/tools/`
2. Follow the decorator pattern for consistency
3. Test thoroughly with the Inspector
4. Monitor performance in the Admin UI or check logs for performance metrics

For more details on creating custom tools, see the [Decorator Patterns](../DECORATOR_PATTERNS.md) documentation.