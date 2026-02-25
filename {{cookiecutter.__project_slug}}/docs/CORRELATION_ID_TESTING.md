# Correlation ID Testing Documentation

## Overview

The `test_correlation_id_integration.py` script is an **integration test** that validates the complete correlation ID flow from MCP client through server to the SQLite logging database. It ensures that correlation IDs—whether provided by the client or auto-generated—are correctly captured and persisted.

**Key Features:**

- **End-to-End Testing**: Tests the complete request lifecycle
- **Dual Mode Testing**: Validates both client-provided and auto-generated correlation IDs
- **SQLite Verification**: Queries the database to confirm persistence
- **All Tools Coverage**: Tests every example tool in the project
- **Visual Results**: Rich console output with tables and status indicators

## What the Script Does

```
┌─────────────────────┐
│   Integration Test  │
│   Script Starts     │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐     ┌──────────────────┐
│  Start MCP Server   │────▶│  Server Process  │
│  (Subprocess)       │     │  (stdio transport)│
└──────────┬──────────┘     └──────────────────┘
           │
           ▼
┌─────────────────────┐
│  Connect as Client  │
│  (MCP stdio_client) │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Call Tools with    │
│  Correlation IDs    │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐     ┌──────────────────┐
│  Query SQLite DB    │────▶│  Verify Logs     │
│  for Each ID        │     │  Present         │
└─────────────────────┘     └──────────────────┘
```

### Test Execution Flow

1. **Server Startup**: Launches the MCP server as a subprocess using stdio transport
2. **Client Connection**: Connects via MCP client session
3. **Tool Discovery**: Lists all available tools from the server
4. **Phase 1 - Client IDs**: Calls each tool with a unique client-provided correlation ID
5. **Phase 2 - Auto IDs**: Calls each tool without correlation IDs (testing auto-generation)
6. **Database Verification**: Queries SQLite to verify all IDs were logged
7. **Results Display**: Shows detailed tables with PASS/FAIL status

## Why It Exists

### Problem Solved

Correlation IDs are essential for distributed tracing and request tracking across the MCP ecosystem. This script validates:

1. **Client-Server Contract**: Ensures clients can send correlation IDs that the server recognizes
2. **Persistence Guarantee**: Confirms that correlation IDs are stored in the database
3. **Tool Coverage**: Verifies that ALL tools (not just some) properly handle correlation IDs
4. **Dual Mode Operation**: Tests both manual ID provision and automatic ID generation

### When to Use

**Run this script when:**

- Adding new tools to verify they support correlation IDs
- After modifying the `tool_logger` decorator
- When troubleshooting correlation ID issues
- Before releases to ensure logging integrity
- Validating client implementations

## How to Execute

### Basic Execution

```bash
# Run from project root directory
python test_correlation_id_integration.py
```

**⚠️ Important**: Do NOT use `pytest` to run this script. It is a standalone integration test:

```bash
# ❌ INCORRECT - Will fail with fixture error
pytest test_correlation_id_integration.py

# ✅ CORRECT - Run as standalone script
python test_correlation_id_integration.py
```

### With Custom Server Module

```bash
python test_correlation_id_integration.py --server-module my_project.server.app
```

### Requirements

- Project dependencies installed (`pip install -e .`)
- Run from project root directory
- SQLite logging enabled in configuration

## Tests Performed

### Phase 1: Client-Provided Correlation IDs

Each tool is called with a specific correlation ID provided in the request metadata:

| Tool                         | Correlation ID        | Arguments                            |
| ---------------------------- | --------------------- | ------------------------------------ |
| `echo`                       | `test_echo_abc123`    | `{"message": "Testing..."}`          |
| `get_time`                   | `test_time_def456`    | `{}`                                 |
| `random_number`              | `test_random_ghi789`  | `{"min_value": 1, "max_value": 100}` |
| `calculate_fibonacci`        | `test_fib_jkl012`     | `{"n": 10}`                          |
| `simulate_heavy_computation` | `test_compute_mno345` | `{"kwargs_list": [...]}`             |
| `process_batch_data`         | `test_batch_pqr678`   | `{"kwargs_list": [...]}`             |

**Verification:**

- Queries SQLite for each correlation ID
- Checks logs exist with correct tool name
- Displays execution timestamp and duration
- Reports PASS/FAIL for each tool

### Phase 2: Auto-Generated Correlation IDs

Each tool is called WITHOUT providing a correlation ID:

**Expected Behavior:**

- Server auto-generates ID in format `req_xxxxxxxxxxxx`
- ID is logged with tool execution
- Format follows ULID-like pattern (12 chars after `req_`)

**Verification:**

- Retrieves most recent log for each tool
- Checks ID starts with `req_`
- Validates format and presence
- Reports PASS/FAIL for auto-generation

## Interpreting Results

### Success Output

```
✅ SUCCESS: All client-provided correlation IDs were properly logged!
✅ SUCCESS: All tools auto-generated correlation IDs correctly!
```

This means:

- All 6 tools accepted and logged client-provided IDs
- All 6 tools generated valid IDs when none provided
- SQLite database contains all expected log entries

### Failure Scenarios

**If some IDs not found:**

```
❌ FAILURE: Some client-provided correlation IDs were not found in logs
```

**Troubleshooting:**

1. Check server is using updated `tool_logger` decorator
2. Verify SQLite logging enabled in `config.yaml`
3. Ensure tools have `ctx: Context = None` parameter
4. Check database path for your platform

**If auto-generation fails:**

```
❌ FAILURE: Some tools did not auto-generate correlation IDs correctly
```

**Troubleshooting:**

1. Verify `tool_logger` decorator is applied to all tools
2. Check `correlation.py` module is properly imported
3. Ensure Context parameter exists for ID extraction

## Manual Verification

After running the test, you can manually verify results:

### Using Streamlit UI

```bash
streamlit run {{ cookiecutter.__project_slug }}/ui/app.py
```

Navigate to the Logs page and filter by these correlation IDs:

- `test_echo_abc123`
- `test_time_def456`
- `test_random_ghi789`
- `test_fib_jkl012`
- `test_compute_mno345`
- `test_batch_pqr678`

### Using SQLite CLI

```bash
# Find database location
python -c "import platformdirs; print(platformdirs.user_data_dir('{{ cookiecutter.__project_slug }}'))"

# Query logs
sqlite3 /path/to/unified_logs.db "SELECT * FROM unified_logs WHERE correlation_id LIKE 'test_%';"
```

### Using Python

```python
import sqlite3
from pathlib import Path
import platformdirs

# Get database path
app_data = platformdirs.user_data_dir("{{ cookiecutter.__project_slug }}")
db_path = Path(app_data) / "unified_logs.db"

# Query specific correlation ID
conn = sqlite3.connect(db_path)
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

cursor.execute("""
    SELECT timestamp, tool_name, status, duration_ms
    FROM unified_logs
    WHERE correlation_id = 'test_echo_abc123'
""")

for row in cursor.fetchall():
    print(f"{row['timestamp']}: {row['tool_name']} - {row['status']}")

conn.close()
```

## Troubleshooting

### Error: `fixture 'server_script_path' not found`

**Cause**: Running with pytest instead of python

**Solution**:

```bash
# ❌ Wrong
pytest test_correlation_id_integration.py

# ✅ Correct
python test_correlation_id_integration.py
```

### Error: Database not found

**Symptom**: "Database not found at /path/to/unified_logs.db"

**Solutions**:

1. Run the server at least once to create the database:

   ```bash
   {{ cookiecutter.__project_slug }}-server --transport stdio
   ```

2. Check configuration enables SQLite logging

3. Verify write permissions on data directory

### Error: Server fails to start

**Symptom**: Test hangs or shows connection errors

**Solutions**:

1. Check server module path is correct
2. Ensure all dependencies installed: `pip install -e .`
3. Verify no other server is using the same port (if using SSE)
4. Check Python version compatibility (3.11-3.13)

### Error: Logs not appearing

**Symptom**: Tests pass but SQLite shows no logs

**Solutions**:

1. **Most Common**: Tools missing `ctx: Context = None` parameter

   ```python
   # ✅ Correct
   async def my_tool(param: str, ctx: Context = None) -> dict:
       ...

   # ❌ Incorrect - won't capture client correlation IDs
   async def my_tool(param: str) -> dict:
       ...
   ```

2. Check `tool_logger` decorator is applied

3. Verify Context import: `from fastmcp import Context`

4. Add delay after tool calls (script already does this)

## Integration with Other Components

### Relation to UNIFIED_LOGGING.md

This test validates the concepts described in [UNIFIED_LOGGING.md](./UNIFIED_LOGGING.md):

- Correlation ID propagation (Section: Correlation IDs)
- SQLite storage (Section: Database Schema)
- Tool logging (Section: With the Tool Logger Decorator)

### Decorator Testing

Validates patterns from [DECORATOR_PATTERNS.md](./DECORATOR_PATTERNS.md):

- `@tool_logger` decorator functionality
- Proper handling of Context parameter
- Error handling and logging

### Streamlit UI Verification

The test provides correlation IDs that can be used to verify the [Streamlit UI](MCP_INSPECTOR_GUIDE.md):

1. Run test to populate database
2. Open Streamlit UI
3. Filter by test correlation IDs
4. Verify logs display correctly

## Best Practices

1. **Run Before Releases**: Always execute before deploying to production
2. **After Tool Changes**: Run when adding/modifying tools
3. **Clean Database**: Start with fresh database for consistent results
4. **Check All Tools**: Ensure every tool passes both test phases
5. **Verify Manually**: Use UI/SQLite to double-check results

## Example Output

```
🧪 Correlation ID Integration Test
Starting MCP server from: {{ cookiecutter.__project_slug }}.server.app

Found 10 tools

Testing all example tools:
→ Calling 'echo' with correlation ID: test_echo_abc123
✓ echo completed successfully
→ Calling 'get_time' with correlation ID: test_time_def456
✓ get_time completed successfully
...

                          SQLite Log Verification
┏━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━┓
┃ Tool            ┃ Expected ID      ┃ Found in DB ┃ Status ┃
┡━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━┩
│ echo            │ test_echo_abc123 │ ✓ Yes       │ PASSED │
│ get_time        │ test_time_def456 │ ✓ Yes       │ PASSED │
...
└─────────────────┴──────────────────┴─────────────┴────────┘

✅ SUCCESS: All client-provided correlation IDs were properly logged!

================================================================================

Testing all example tools WITHOUT client-provided correlation IDs:
...
✅ SUCCESS: All tools auto-generated correlation IDs correctly!
```

## Future Enhancements

Potential improvements to the test script:

1. **Parallel Testing**: Test multiple tools concurrently
2. **Stress Testing**: High-volume correlation ID generation
3. **Custom Assertions**: More detailed validation of log content
4. **Report Generation**: Export results to file
5. **CI Integration**: Return exit codes for automated testing

## See Also

- [Unified Logging](./UNIFIED_LOGGING.md) - Detailed logging system documentation
- [Decorator Patterns](./DECORATOR_PATTERNS.md) - Tool decorator usage
- [MCP Inspector Guide](./MCP_INSPECTOR_GUIDE.md) - UI testing and verification
