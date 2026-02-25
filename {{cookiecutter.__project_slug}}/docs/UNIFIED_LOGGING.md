# Unified Logging System Documentation

## Overview

The {{ cookiecutter.project_name }} implements a unified logging system that captures both tool executions and internal application logs in a single, queryable database. The system features:

- **Correlation IDs**: Track related events across the entire request lifecycle
- **Pluggable Destinations**: Easily swap between different log storage backends
- **Unified Schema**: All log types use the same structure for consistency
- **Thread-Safe**: Proper isolation between concurrent requests
- **Developer-Friendly API**: Simple functions for tool developers

## Architecture

```
┌─────────────────────┐     ┌──────────────────┐
│   Tool/App Code     │────▶│  Unified Logger  │
└─────────────────────┘     └────────┬─────────┘
                                     │
                            ┌────────▼─────────┐
                            │  LogDestination  │
                            │   Interface      │
                            └────────┬─────────┘
                                     │
                ┌────────────────────┼────────────────────┐
                │                    │                    │
        ┌───────▼────────┐  ┌───────▼────────┐  ┌───────▼────────┐
        │SQLiteDestination│  │  ElasticSearch  │  │    Postgres     │
        │  (Version 1)    │  │  (Future)       │  │    (Future)     │
        └────────────────┘  └────────────────┘  └────────────────┘
```

## Key Components

### 1. Correlation IDs

Every tool request gets a unique correlation ID in the format `req_xxxxxxxxxxxx`. This ID is automatically propagated to all related logs.

**Client-Provided vs Auto-Generated Correlation IDs**

The system supports two modes of correlation ID management:

1. **Client-Provided IDs**: When an MCP client includes a correlation ID in the request metadata, the system will use it for all related logs. This allows tracking requests across client and server boundaries.

2. **Auto-Generated IDs**: When no correlation ID is provided by the client, the system automatically generates one in the format `req_xxxxxxxxxxxx`.

**Important: Context Parameter Requirement**

For client-provided correlation IDs to work, your tools MUST include a `ctx: Context = None` parameter:

```python
from fastmcp import Context

# ✅ CORRECT - Can receive client correlation IDs
async def my_tool(param: str, ctx: Context = None) -> dict:
    # Tool implementation
    return {"result": "success"}

# ❌ INCORRECT - Will only use auto-generated IDs
async def my_tool(param: str) -> dict:
    # Tool implementation
    return {"result": "success"}
```

The `tool_logger` decorator automatically extracts the correlation ID from the Context metadata when available.

```python
from {{ cookiecutter.__project_slug }}.log_system import set_correlation_id, get_correlation_id

# Set a new correlation ID (usually done automatically)
correlation_id = set_correlation_id()

# Get the current correlation ID
current_id = get_correlation_id()
```

### 2. Log Entry Structure

All logs use a unified `LogEntry` dataclass:

```python
@dataclass
class LogEntry:
    correlation_id: str      # Unique request identifier
    timestamp: datetime      # When the log was created
    level: str              # DEBUG, INFO, WARNING, ERROR, CRITICAL
    log_type: str           # tool_execution, internal, framework
    message: str            # Log message
    tool_name: Optional[str] # Name of the tool (if applicable)
    duration_ms: Optional[float] # Execution duration
    status: Optional[str]   # success, error, running
    input_args: Optional[Dict[str, Any]] # Tool inputs
    output_summary: Optional[str] # Tool output summary
    error_message: Optional[str] # Error details
    # ... additional fields
```

### 3. Log Types

- **tool_execution**: Logs from MCP tool executions
- **internal**: Application logs from your code
- **framework**: MCP framework and system logs

## Usage for Tool Developers

### Basic Logging

```python
from {{ cookiecutter.__project_slug }}.log_system import get_tool_logger
from fastmcp import Context

async def my_custom_tool(param: str, ctx: Context = None) -> str:
    logger = get_tool_logger("my_custom_tool")

    logger.debug(f"Received parameter: {param}")

    try:
        # Tool logic
        result = process_data(param)
        logger.info(f"Successfully processed {len(result)} items")
        return result
    except Exception as e:
        logger.error(f"Failed to process: {e}")
        raise
```

**Remember**: Always include the `ctx: Context = None` parameter to support client-provided correlation IDs.

### With the Tool Logger Decorator

The `@tool_logger` decorator automatically handles correlation IDs and tool execution logging:

```python
from {{ cookiecutter.__project_slug }}.decorators import tool_logger
from fastmcp import Context

@tool_logger
async def my_tool(data: str, ctx: Context = None) -> dict:
    # Your tool logic here
    return {"result": "success"}
```

This automatically logs:

- Correlation ID (extracted from Context or auto-generated)
- Tool start with status "running"
- Input parameters
- Execution duration
- Success/error status
- Output summary

**Note**: The Context parameter is essential for receiving client-provided correlation IDs. Without it, the system will always generate new IDs.

### Manual Correlation Context

For complex workflows, you can manually manage correlation context:

```python
from {{ cookiecutter.__project_slug }}.log_system import CorrelationContext, get_tool_logger

async def complex_workflow():
    async with CorrelationContext() as correlation_id:
        logger = get_tool_logger("workflow")

        logger.info(f"Starting workflow with ID: {correlation_id}")

        # All logs within this context share the same correlation ID
        await step1()
        await step2()

        logger.info("Workflow completed")
```

## Database Schema

The SQLite destination uses the following schema:

```sql
CREATE TABLE unified_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    correlation_id TEXT NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    level TEXT NOT NULL,
    log_type TEXT CHECK(log_type IN ('tool_execution', 'internal', 'framework')),
    message TEXT NOT NULL,
    tool_name TEXT,
    duration_ms REAL,
    status TEXT CHECK(status IN ('success', 'error', 'running', NULL)),
    input_args TEXT,  -- JSON
    output_summary TEXT,
    error_message TEXT,
    module TEXT,
    function TEXT,
    line INTEGER,
    thread_name TEXT,
    process_id INTEGER,
    extra_data TEXT,  -- JSON
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

## Querying Logs

### From Python Code

```python
from {{ cookiecutter.__project_slug }}.log_system.destinations import SQLiteDestination
from {{ cookiecutter.__project_slug }}.config import get_config

# Get the destination
config = get_config()
destination = SQLiteDestination(config)

# Query by correlation ID
logs = await destination.query(correlation_id="req_a1b2c3d4e5f6")

# Query by tool name
tool_logs = await destination.query(tool_name="my_tool", limit=100)

# Query by time range
from datetime import datetime, timedelta
recent_logs = await destination.query(
    start_time=datetime.now() - timedelta(hours=1),
    limit=1000
)

# Get statistics
stats = destination.get_statistics()
```

### From Streamlit UI

The admin UI provides a comprehensive log viewer at `/logs` with:

- Real-time log display
- Filtering by level, type, status, and time range
- Search by correlation ID, tool name, or message
- Export capabilities (CSV, JSON, Excel)

## Configuration

The logging system uses configuration from `ServerConfig`:

```yaml
log_level: INFO
log_retention_days: 30
```

## Migration from Old System

If you have existing logs in the old `logs.db` format:

1. The old logs remain in `logs.db`
2. New logs go to `unified_logs.db`
3. Both can coexist during transition
4. Consider writing a migration script if needed

## Future Destinations

The architecture supports adding new destinations without changing application code:

```python
# Future: Elasticsearch destination
class ElasticsearchDestination(LogDestination):
    async def write(self, entry: LogEntry) -> None:
        # Send to Elasticsearch
        pass

# Just change initialization
destination = ElasticsearchDestination(config)
UnifiedLogger.initialize(destination)
```

## Best Practices

1. **Use Correlation IDs**: They make debugging much easier
2. **Log Levels**: Use appropriate levels (DEBUG for details, INFO for flow, ERROR for failures)
3. **Structured Data**: Include relevant context in extra_data
4. **Tool Names**: Use consistent, descriptive tool names
5. **Error Messages**: Include enough detail for debugging

## Troubleshooting

### Logs Not Appearing

1. Check the database file exists: `data_dir/unified_logs.db`
2. Verify UnifiedLogger is initialized in server startup
3. Check log level configuration

### Correlation IDs Not Working

1. **Most Common Issue**: Ensure all tools have `ctx: Context = None` parameter
2. Verify the Context is imported from `mcp.server.fastmcp`
3. Check that the tool logger decorator is applied
4. Verify the MCP client is sending correlation IDs in metadata
5. Note: MCP Inspector does not provide UI for setting correlation IDs

### Performance Issues

1. Use appropriate query limits
2. Add indexes for frequently queried fields
3. Consider log rotation/cleanup strategies
