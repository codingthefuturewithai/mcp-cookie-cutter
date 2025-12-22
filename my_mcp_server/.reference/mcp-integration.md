# MCP Integration Reference

This document explains how decorators integrate with the MCP protocol in this template. It's designed for AI assistants to understand the specific patterns and requirements.

## The Integration Challenge

MCP has specific requirements:
1. Tools must have inspectable signatures (not **kwargs)
2. Parameters arrive as strings from clients
3. Errors must be properly formatted
4. All operations should be logged

The decorators add:
1. Automatic type conversion
2. Comprehensive logging
3. Exception handling
4. Optional parallelization

The challenge: Apply decorators WITHOUT breaking MCP's requirements.

## The Solution: Decorator Chain

### Order of Application (CRITICAL)

```python
# For regular tools:
tool → type_converter → tool_logger → exception_handler → MCP

# For parallel tools:
tool → type_converter → parallelize → tool_logger → exception_handler → MCP
```

### Why This Order?

1. **type_converter** FIRST: Converts MCP's string parameters to correct types
2. **parallelize** (if needed): Wraps for batch processing
3. **tool_logger**: Records execution with converted parameters
4. **exception_handler** LAST: Catches any errors and re-raises for MCP

## Decorator Behaviors

### 1. type_converter Decorator

**Purpose**: Handle MCP's string parameters automatically

```python
# MCP sends:
{"message": "hello", "count": "5", "enabled": "true"}

# type_converter converts to:
{"message": "hello", "count": 5, "enabled": True}
```

**Key Features**:
- Inspects function annotations
- Converts strings to expected types
- Handles optional parameters
- Preserves Context parameter

### 2. tool_logger Decorator

**Purpose**: Log all tool executions to SQLite

**What it logs**:
- Tool name
- Input parameters (after conversion)
- Execution time
- Output summary
- Errors (if any)
- Correlation ID for request tracking

**Key Features**:
- Non-blocking logging
- Automatic timestamp
- Truncates large outputs
- Links related operations

### 3. exception_handler Decorator

**Purpose**: Ensure errors are properly handled for MCP

**Behavior**:
1. Catches any exception
2. Logs error details
3. **RE-RAISES** the exception
4. MCP catches it and sets `isError = True`

**Why re-raise?**
- MCP expects to handle errors itself
- Provides consistent error format to clients
- Maintains protocol compliance

### 4. parallelize Decorator (Optional)

**Purpose**: Enable batch processing for appropriate tools

**When to use**:
- Tool processes lists of independent items
- Each item can be processed separately
- Order doesn't matter

**When NOT to use**:
- Single item processing
- Sequential operations
- Stateful operations

## Registration Pattern

### How Tools Are Registered

```python
def register_tools(mcp_server: FastMCP, config: ServerConfig) -> None:
    # Import decorators
    from decorators.exception_handler import exception_handler
    from decorators.tool_logger import tool_logger
    from decorators.type_converter import type_converter
    
    # For each tool
    for tool_func in example_tools:
        # Apply decorator chain
        decorated = exception_handler(
            tool_logger(
                type_converter(tool_func),
                config.__dict__
            )
        )
        
        # Register with MCP
        mcp_server.tool(name=tool_func.__name__)(decorated)
```

### Why This Works

1. **Preserves Signatures**: Each decorator uses `functools.wraps`
2. **Maintains Introspection**: MCP can still see parameter names/types
3. **Adds Functionality**: Without breaking MCP protocol
4. **Handles Errors**: In MCP-compliant way

## Common Integration Issues

### Issue 1: Generic "kwargs" in MCP Inspector

**Symptom**: MCP Inspector shows `kwargs` instead of parameter names
**Cause**: Decorator not preserving function signature
**Solution**: Ensure all decorators use `functools.wraps`

### Issue 2: Type Errors with Parameters

**Symptom**: "invalid literal for int()" errors
**Cause**: type_converter not applied or not working
**Solution**: Ensure type_converter is first in chain

### Issue 3: Errors Not Showing in Client

**Symptom**: Tool fails silently
**Cause**: Exception being swallowed, not re-raised
**Solution**: exception_handler must re-raise after logging

### Issue 4: Context Parameter Issues

**Symptom**: "unexpected keyword argument 'ctx'"
**Cause**: Context not properly handled in decorator
**Solution**: Decorators must preserve Context parameter

## The Context Parameter Convention

### How Context Works

1. MCP provides Context to tools that request it
2. Parameter name can be anything: `ctx`, `context`, `mcp_context`
3. Must have type annotation: `Context`
4. Should have default: `= None`

### Decorator Handling

Each decorator must:
1. Check if function expects Context
2. Extract Context from kwargs if present
3. Pass Context through properly
4. Not include Context in logged parameters

## Parallel Processing Pattern

### When Parallel Makes Sense

```python
# GOOD: Independent items
async def process_files(file_paths: list, ctx: Context = None) -> list:
    # Each file processed independently
    results = []
    for path in file_paths:
        results.append(await process_file(path))
    return results

# BAD: Sequential dependency
async def build_report(sections: list, ctx: Context = None) -> str:
    # Each section depends on previous
    report = ""
    for section in sections:
        report += format_section(section, previous=report)
    return report
```

### Parallel Decorator Behavior

1. Receives list of items
2. Creates worker pool
3. Distributes items to workers
4. Collects results in order
5. Returns combined results

## Testing Integration

### Verify Decorator Chain

```python
# In tests/integration/test_example_tools_integration.py
async def test_decorator_chain():
    # Test that decorators are applied correctly
    session = await create_test_session()
    
    # Test type conversion
    result = await session.call_tool("echo_tool", {"message": "test"})
    assert result.content[0].text == "Echo: test"
    
    # Test error handling
    result = await session.call_tool("random_number", {
        "min_value": "10",
        "max_value": "5"  # Invalid range
    })
    assert result.isError is True
```

### Verify MCP Compliance

1. **Parameter Discovery**: Check MCP Inspector shows correct parameters
2. **Type Handling**: Test with string inputs
3. **Error Reporting**: Verify errors appear in client
4. **Context Usage**: Test logging appears in client

## For AI Assistants

When working with MCP integration:

1. **Never manually apply decorators in tools** - Server does this
2. **Always put type_converter first** - It handles MCP's strings
3. **Expect re-raised exceptions** - This is correct behavior
4. **Preserve Context parameter** - It's optional but important
5. **Test with real MCP client** - Not just unit tests

## Key Takeaways

1. **Decorator order matters**: type_converter → logger → exception_handler
2. **Signatures must be preserved**: Use functools.wraps
3. **Exceptions are re-raised**: For MCP compliance
4. **Context is special**: Handle it separately
5. **Test the full chain**: Integration tests are critical