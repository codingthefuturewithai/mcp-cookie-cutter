# MCP Client Integration Testing Guide

## Overview and Intention

This document describes the MCP (Model Context Protocol) client integration testing approach implemented in this MCP Server template. These integration tests are designed to validate that MCP tools work correctly when accessed through the actual MCP client protocol, exactly as they would be used by real MCP clients such as Claude Code, Cursor, Continue, and other AI-powered development tools.

### Why Integration Testing Matters for MCP Servers

While unit tests verify that individual decorators and functions work correctly in isolation, integration tests validate the complete end-to-end flow:

1. **Protocol Compliance**: Ensures tools are discoverable and callable via the MCP protocol
2. **Parameter Serialization**: Validates that string parameters from MCP clients are correctly converted to typed parameters
3. **Error Handling**: Confirms that exceptions are properly formatted and returned as MCP error responses
4. **Decorator Integration**: Tests that decorators (exception_handler, tool_logger, parallelize) work correctly in the full MCP context
5. **Real Client Behavior**: Mirrors how actual MCP clients interact with the server

## Architectural Design

### Core Components

```
tests/integration/
├── test_example_tools_integration.py    # Example tools integration tests
├── MCP_INTEGRATION_TESTING_GUIDE.md  # This document
└── (generated during testing)
    ├── .coverage.*             # Coverage data from subprocesses
    └── htmlcov/                # HTML coverage reports
```

### Key Design Decisions

1. **Subprocess Architecture**: The MCP server runs as a subprocess, exactly as it would when launched by a real MCP client
2. **STDIO Transport**: Uses standard input/output for communication, the most common MCP transport
3. **anyio Framework**: Leverages anyio instead of pytest-asyncio to avoid async context teardown issues
4. **Explicit Session Management**: Each test explicitly creates and cleans up its session to ensure proper resource management

## Implementation Details

### Session Creation Pattern

```python
async def create_test_session():
    """Create an MCP client session for testing."""
    # Create server parameters for stdio connection
    server_params = StdioServerParameters(
        command=sys.executable,
        args=["-m", server_module],
        env=None
    )
    
    # Start the stdio client
    stdio_context = stdio_client(server_params)
    read, write = await stdio_context.__aenter__()
    
    # Create and initialize session
    session = ClientSession(read, write)
    await session.__aenter__()
    await session.initialize()
    
    # Return session and cleanup function
    return session, cleanup
```

### Test Structure Pattern

```python
class TestMCPToolExecution:
    async def test_echo_tool_execution(self):
        session, cleanup = await create_test_session()
        try:
            # Test implementation
            result = await session.call_tool("echo_tool", {"message": "Hello"})
            # Assertions
        finally:
            await cleanup()
```

### Key Testing Scenarios

1. **Tool Discovery**
   - Validates all tools are discoverable via `list_tools()`
   - Ensures no "kwargs" parameters in schemas (MCP compatibility)
   - Verifies tool metadata (descriptions, schemas)

2. **Tool Execution**
   - Tests each tool with valid parameters
   - Validates parameter type conversion (strings → typed)
   - Checks response structure and content

3. **Error Handling**
   - Missing required parameters
   - Invalid parameter types
   - Tool exceptions with error format
   - Non-existent tool calls

4. **Protocol Compliance**
   - Sequential tool calls
   - Concurrent tool calls
   - Large parameter handling

## Running the Integration Tests

### Basic Test Execution

```bash
# Navigate to generated project
cd /path/to/your/generated/project

# Activate virtual environment
source .venv/bin/activate  # or .venv\Scripts\activate on Windows

# Run all integration tests
python -m pytest tests/integration/test_example_tools_integration.py -v

# Run specific test class
python -m pytest tests/integration/test_example_tools_integration.py::TestMCPToolDiscovery -v

# Run specific test
python -m pytest tests/integration/test_example_tools_integration.py::TestMCPToolExecution::test_echo_tool_execution -v
```

### Coverage Measurement

Since integration tests spawn subprocesses, measuring coverage requires special configuration:

```bash
# Create .coveragerc file (included in template)
[run]
source = your_project_name
parallel = true
concurrency = multiprocessing

# Create sitecustomize.py
import coverage
coverage.process_startup()

# Run with coverage tracking
export COVERAGE_PROCESS_START=/path/to/.coveragerc
coverage erase
coverage run -m pytest tests/integration/test_example_tools_integration.py -v
coverage combine
coverage report
coverage html
```

## Understanding the Test Flow

### 1. Subprocess Spawning

When a test calls `create_test_session()`, it:
- Spawns a new Python subprocess running the MCP server module
- Establishes STDIO pipes for bidirectional communication
- The server runs in a completely isolated process, just like with real MCP clients

### 2. MCP Protocol Handshake

The test client:
- Sends an `initialize` request with client capabilities
- Receives server capabilities and metadata
- Completes the handshake with an `initialized` notification

### 3. Tool Interaction

Tests interact with tools using the official MCP client SDK:
```python
# List available tools
tools_response = await session.list_tools()

# Call a tool with parameters
result = await session.call_tool("tool_name", {"param": "value"})

# Check for errors
if result.isError:
    error_text = extract_error_text(result)
```

### 4. Cleanup

Each test ensures proper cleanup:
- Closes the client session
- Terminates the subprocess
- Releases all resources

## Critical Implementation Nuances

### 1. String Parameter Conversion

MCP clients send all parameters as strings. The parallelize decorator includes type conversion:

```python
# In parallelize.py decorator
if param.annotation == int and isinstance(param_value, str):
    converted_kwargs[param_name] = int(param_value)
elif param.annotation == float and isinstance(param_value, str):
    converted_kwargs[param_name] = float(param_value)
elif param.annotation == bool and isinstance(param_value, str):
    converted_kwargs[param_name] = param_value.lower() in ('true', '1', 'yes')
```

### 2. Parallel Tool Results

Parallel tools return multiple `TextContent` items, one per result:

```python
# Extract all results from parallel tool
results = []
for content in result.content:
    if isinstance(content, types.TextContent):
        try:
            results.append(json.loads(content.text))
        except json.JSONDecodeError:
            pass
```

### 3. Error Response Handling

Tools may return errors in different ways:
- `result.isError = True` with error content
- Exception format in response content
- Standard error keywords in text

### 4. Async Context Management

We use anyio instead of pytest-asyncio to avoid teardown errors:
- No class-level async fixtures
- Explicit session creation/cleanup in each test
- Compatible with subprocess lifecycle

## Adding Tests for New Tools

When you add new tools to your MCP server, follow these patterns:

### 1. Basic Tool Test

```python
async def test_my_new_tool(self):
    """Test my_new_tool execution."""
    session, cleanup = await create_test_session()
    try:
        # Call with appropriate parameters
        result = await session.call_tool("my_new_tool", {
            "param1": "value1",
            "param2": "123"  # Numbers as strings
        })
        
        # Verify success
        assert not result.isError, f"Tool failed: {result}"
        
        # Extract and validate response
        text_content = self._extract_text_content(result)
        data = json.loads(text_content)
        assert data["expected_field"] == expected_value
    finally:
        await cleanup()
```

### 2. Error Handling Test

```python
async def test_my_tool_error_handling(self):
    """Test error handling for my_tool."""
    session, cleanup = await create_test_session()
    try:
        # Call with invalid parameters
        result = await session.call_tool("my_tool", {
            "invalid_param": "bad_value"
        })
        
        # Should return error
        assert result.isError, "Should return error"
        
        # Verify error message
        error_text = self._extract_error_text(result)
        assert "expected error keyword" in error_text.lower()
    finally:
        await cleanup()
```

### 3. Parallel Tool Test

```python
async def test_my_parallel_tool(self):
    """Test parallel tool execution."""
    session, cleanup = await create_test_session()
    try:
        kwargs_list = [
            {"input": "data1"},
            {"input": "data2"},
            {"input": "data3"}
        ]
        
        result = await session.call_tool("my_parallel_tool", {
            "kwargs_list": kwargs_list
        })
        
        # Extract multiple results
        results = []
        for content in result.content:
            if isinstance(content, types.TextContent):
                results.append(json.loads(content.text))
        
        # Verify all results received
        assert len(results) == len(kwargs_list)
    finally:
        await cleanup()
```

## Troubleshooting

### Common Issues

1. **Import Errors**
   - Ensure virtual environment is activated
   - Check that all dependencies are installed
   - Verify the server module path is correct

2. **Subprocess Timeout**
   - Server may be taking too long to start
   - Check for errors in server initialization
   - Increase timeout in stdio_client if needed

3. **Coverage Not Tracking Subprocess**
   - Ensure COVERAGE_PROCESS_START is set
   - Verify sitecustomize.py is in Python path
   - Check .coveragerc configuration

4. **Async Teardown Errors**
   - Make sure you're using the anyio pattern
   - Don't use pytest fixtures for session management
   - Always call cleanup in finally block

### Debugging Tips

1. **Enable Debug Logging**
   ```python
   import logging
   logging.basicConfig(level=logging.DEBUG)
   ```

2. **Print Subprocess Output**
   - Modify stdio_client to capture stderr
   - Add print statements in server code
   - Check server logs in SQLite database

3. **Test in Isolation**
   ```bash
   # Test single tool to isolate issues
   python -m pytest tests/integration/test_example_tools_integration.py::TestMCPToolExecution::test_specific_tool -v -s
   ```

## Best Practices

1. **Always Test Real Scenarios**: Write tests that mirror actual client usage
2. **Validate Response Structure**: Check both success and error response formats
3. **Test Edge Cases**: Empty parameters, large inputs, concurrent calls
4. **Document Expected Behavior**: Use clear test names and docstrings
5. **Handle Cleanup Properly**: Always use try/finally for session cleanup
6. **Test Conditionally**: Use template variables for optional features

## Conclusion

The MCP integration testing framework provides confidence that your MCP server will work correctly with real clients. By testing through the actual protocol with subprocess isolation, these tests catch issues that unit tests might miss, ensuring a robust and reliable MCP server implementation.

Remember: Integration tests complement but don't replace unit tests. Use both for comprehensive coverage of your MCP server functionality.