# Decorator Patterns in {{ cookiecutter.project_name }}

This document explains the SAAGA decorator patterns used in your MCP server and provides guidance on the async-only patterns and parallel tool calling conventions.

## Overview

Your MCP server automatically applies decorators to all tools. These decorators follow strict async-only patterns and provide:

- **Exception handling**: Standard error responses
- **Logging**: Comprehensive execution tracking with SQLite persistence
- **Parallelization**: Concurrent execution with signature transformation

## ⚠️ IMPORTANT: Async-Only Pattern

**All tools must be async functions.** The decorators only support async functions for consistency and performance.

```python
# ✅ CORRECT - Async function
async def my_tool(param: str) -> dict:
    return {"result": param.upper()}

# ❌ INCORRECT - Sync function (will cause errors)
def my_tool(param: str) -> dict:
    return {"result": param.upper()}
```

## The Three Decorators

### 1. Exception Handler (Applied to ALL tools)

The exception handler ensures consistent error handling:

```python
@exception_handler
async def my_tool(param: str) -> dict:
    if not param:
        raise ValueError("Parameter required")
    return {"result": param.upper()}
```

**Error Format:**

```python
{
    "Status": "Exception",
    "Message": "Parameter required",
    "ExceptionType": "ValueError",
    "Traceback": "Full stack trace..."
}
```

**What it does:**

- Catches any exception thrown by your tool
- Returns standard error response format
- Logs the error with full stack trace
- Your tool can raise exceptions freely

### 2. Tool Logger (Applied to ALL tools)

Tracks execution metrics and logs all tool invocations to SQLite database.

**IMPORTANT: Context Parameter Requirement**

For correlation IDs to work properly with MCP clients that provide them, all tools MUST include a `ctx: Context = None` parameter:

```python
from fastmcp import Context

# ✅ CORRECT - Includes Context parameter
async def my_tool(param: str, ctx: Context = None) -> dict:
    # Logger tracks:
    # - Correlation ID (from Context or auto-generated)
    # - Start time
    # - Input parameters (JSON serialized)
    # - Execution duration (milliseconds)
    # - Output (summarized)
    # - Any errors
    return {"result": "processed"}

# ❌ INCORRECT - Missing Context parameter (correlation IDs won't work)
async def my_tool(param: str) -> dict:
    return {"result": "processed"}
```

The Context parameter:

- Must be imported from `mcp.server.fastmcp`
- Should be the last parameter in the function signature
- Should have a default value of `None`
- Will be automatically provided by the MCP runtime when available
- Contains metadata including client-provided correlation IDs

When a client provides a correlation ID in the request metadata, the tool_logger decorator will extract it from the Context and use it for all related logs. If no correlation ID is provided, the system will auto-generate one.

**What it logs:**

- Correlation ID (client-provided or auto-generated)
- Tool name and parameters
- Execution time in milliseconds
- Success/failure status
- Output summary (first 500 chars)
- Error messages and stack traces

### 3. Parallelize (Applied ONLY to specific tools)

**⚠️ IMPORTANT**: This decorator is only applied to tools in the `parallel_example_tools` list and **transforms the function signature**.

## 🔄 Signature Transformation

The parallelize decorator transforms your function signature:

```python
# Your original function (single item processing)
async def process_item(item: str, operation: str = "upper") -> str:
    if operation == "upper":
        return item.upper()
    elif operation == "lower":
        return item.lower()
    else:
        raise ValueError(f"Unknown operation: {operation}")

# After parallelize decorator, the signature becomes:
# async def process_item(kwargs_list: List[Dict]) -> List[str]
```

## 📞 How to Call Parallel Tools

### In MCP Inspector or Client:

```python
# Call parallel tool with List[Dict] format
result = await process_item([
    {"item": "hello", "operation": "upper"},
    {"item": "world", "operation": "lower"},
    {"item": "test", "operation": "upper"}
])

# Returns: ["HELLO", "world", "TEST"]
```

### Error Handling in Parallel Tools:

```python
# If one item fails, it returns error format
result = await process_item([
    {"item": "hello", "operation": "upper"},
    {"item": "world", "operation": "invalid"}  # This will fail
])

# Returns:
# [
#   "HELLO",
#   {
#     "Status": "Exception",
#     "Message": "Unknown operation: invalid",
#     "ExceptionType": "ValueError",
#     "Index": 1
#   }
# ]
```

## When to Use the Parallelize Decorator

The parallelize decorator is **NOT** suitable for all tools. Use it ONLY when:

### ✅ Good Candidates for Parallelization

1. **Batch Processing Tools**

   ```python
   async def process_single_item(item: str) -> dict:
       """Process one item - will be parallelized automatically."""
       return {"processed": expensive_computation(item)}
   ```

2. **Independent Computations**

   ```python
   async def analyze_document(doc_id: str) -> dict:
       """Analyze one document - will be parallelized automatically."""
       return analyze_single_doc(doc_id)
   ```

3. **Parallel API Calls**
   ```python
   async def fetch_resource(url: str) -> dict:
       """Fetch one URL - will be parallelized automatically."""
       return await fetch_url(url)
   ```

### ❌ Bad Candidates for Parallelization

1. **Sequential Operations**

   ```python
   async def sequential_process(data: str) -> str:
       """Operations that depend on order."""
       step1 = await process_step1(data)
       step2 = await process_step2(step1)  # Depends on step1
       return await process_step3(step2)   # Depends on step2
   ```

2. **Shared State Operations**

   ```python
   def update_database(records: List[dict]) -> dict:
       """Operations that modify shared state."""
       # Database transactions need careful handling
       # NOT suitable for naive parallelization
   ```

3. **Single Item Operations**
   ```python
   def get_user_info(user_id: str) -> dict:
       """Single item operations don't benefit."""
       return fetch_user(user_id)
   ```

## How the Parallelize Decorator Works

The decorator detects if the input is iterable (list, tuple, etc.) and processes each item in parallel:

```python
# Original function
def process_item(item: str) -> dict:
    return expensive_computation(item)

# When called with a list, automatically parallelized:
result = process_item(["item1", "item2", "item3"])
# Returns: [result1, result2, result3]
```

## Adding Tools to Your Server

### Regular Tools (Most Common)

Add to the `example_tools` list in `tools/__init__.py`:

```python
# tools/my_tools.py
from fastmcp import Context

async def my_regular_tool(param: str, ctx: Context = None) -> dict:
    """A regular tool with automatic exception handling and logging."""
    return {"processed": param}

# tools/__init__.py
from .my_tools import my_regular_tool
example_tools.append(my_regular_tool)
```

### Parallel Tools (Use Sparingly)

Add to the `parallel_example_tools` list ONLY if suitable:

```python
# tools/batch_tools.py
from fastmcp import Context

async def batch_processor(items: List[str], ctx: Context = None) -> List[dict]:
    """Process multiple items in parallel."""
    # Each item processed independently
    return [{"processed": item} for item in items]

# tools/__init__.py
from .batch_tools import batch_processor
parallel_example_tools.append(batch_processor)
```

## Understanding the Registration Process

Your server's `app.py` automatically applies decorators in the correct order:

```python
# For regular tools:
# exception_handler → tool_logger → your function
decorated = exception_handler(tool_logger(your_tool))

# For parallel tools:
# exception_handler → tool_logger → parallelize → your function
decorated = exception_handler(tool_logger(parallelize(your_tool)))
```

## Common Patterns and Examples

### Pattern 1: Type Conversion with Context

MCP passes parameters as strings. Handle conversion in your tools and always include the Context parameter:

```python
from fastmcp import Context

async def calculate(a: str, b: str, ctx: Context = None) -> dict:
    """Handle string inputs from MCP."""
    try:
        num_a = float(a)
        num_b = float(b)
        return {"sum": num_a + num_b}
    except ValueError as e:
        # Exception handler will catch and format this
        raise ValueError(f"Invalid number format: {e}")
```

### Pattern 2: Async Tools with Context

All tools must be async and include the Context parameter:

```python
from fastmcp import Context

async def fetch_data(url: str, ctx: Context = None) -> dict:
    """Async tools work automatically."""
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return {"data": await response.json()}
```

### Pattern 3: Progress Reporting with Context

For long-running operations, log progress and include the Context parameter:

```python
import logging
from fastmcp import Context

logger = logging.getLogger(__name__)

async def long_operation(data: str, ctx: Context = None) -> dict:
    """Log progress for long operations."""
    logger.info("Starting phase 1...")
    result1 = await phase1(data)

    logger.info("Starting phase 2...")
    result2 = await phase2(result1)

    logger.info("Operation complete")
    return {"result": result2}
```

## Debugging Your Tools

1. **Check MCP Inspector Output**
   - Parameters should show proper names (not "kwargs")
   - Return values should be JSON-serializable

2. **Enable Debug Logging**

   ```bash
   python -m {{ cookiecutter.__project_slug }}.server.app --log-level DEBUG
   ```

3. **Check SQLite Logs**
   - Location: `{{ cookiecutter.__project_slug }}/logs.db`
   - Contains all tool executions with timings

4. **Test Parallelization**
   ```python
   # Test with small batches first
   result = parallel_tool(["item1", "item2"])
   # Verify results are in correct order
   ```

## Best Practices

1. **Always include Context parameter** - Required for correlation ID support
2. **Let exceptions bubble up** - The exception handler will catch them
3. **Return JSON-serializable data** - dict, list, str, int, float, bool
4. **Use type hints** - Helps with documentation and IDE support
5. **Log important operations** - Use the standard logging module
6. **Test with MCP Inspector** - Verify parameters and outputs
7. **Be careful with parallelization** - Only use when truly beneficial

## Summary

- **All tools** get exception handling and logging automatically
- **Only specific tools** get parallelization (those in `parallel_example_tools`)
- Parallelization is for batch/independent operations only
- The decorators preserve function signatures for MCP introspection
- You don't manually apply decorators - the server does it for you
