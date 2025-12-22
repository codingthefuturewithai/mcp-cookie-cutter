# Testing Guide for My MCP Server

## Overview

This project uses a comprehensive testing strategy that includes both unit tests and integration tests to ensure reliability and correctness of the MCP server implementation.

## Test Structure

```
tests/
├── README.md                     # This file
├── conftest.py                   # Pytest configuration and fixtures
├── unit/                         # Unit tests (isolated component testing)
│   ├── __init__.py
│   └── test_decorators.py        # Tests for decorators
└── integration/                  # Integration tests (full MCP protocol testing)
    ├── __init__.py
    ├── test_example_tools_integration.py   # Main MCP protocol tests
    ├── test_example_tools_edge_cases.py    # Edge case and error condition tests
    ├── cli.py                     # Test runner utilities
    ├── COVERAGE_GUIDE.md          # Coverage configuration guide
    └── MCP_INTEGRATION_TESTING_GUIDE.md  # Integration testing details
```

## Running Tests

### Quick Start

```bash
# Run all tests with coverage
uv run pytest tests/ --cov=my_mcp_server --cov-report=term --cov-report=html

# Run only unit tests
uv run pytest tests/unit/ -v

# Run only integration tests
uv run pytest tests/integration/ -v

# Run with verbose output
uv run pytest tests/ -v

# Run a specific test file
uv run pytest tests/integration/test_example_tools_integration.py -v

# Run a specific test
uv run pytest tests/integration/test_example_tools_integration.py::TestMCPToolDiscovery::test_all_tools_discoverable -v
```

### Coverage Reports

After running tests with coverage, you can view the detailed HTML report:

```bash
# Generate HTML coverage report
uv run pytest tests/ --cov=my_mcp_server --cov-report=html

# Open the report (macOS)
open htmlcov/index.html

# Open the report (Linux)
xdg-open htmlcov/index.html
```

## Test Types

### Unit Tests (`tests/unit/`)

Unit tests focus on testing individual components in isolation:

- **Decorators**: Test exception handling, logging, and parallelization decorators
- **Configuration**: Test configuration loading and validation
- **Utilities**: Test helper functions and utilities
- **Tool Logic**: Test individual tool functions without MCP protocol overhead

#### Example Unit Test

```python
@pytest.mark.asyncio
async def test_exception_handler():
    """Test that exception handler formats errors correctly."""
    
    @exception_handler
    async def failing_tool():
        raise ValueError("Test error")
    
    result = await failing_tool()
    assert result["Status"] == "Exception"
    assert "Test error" in result["Message"]
```

### Integration Tests (`tests/integration/`)

Integration tests validate the complete MCP server flow:

- **Protocol Compliance**: Tools are discoverable and callable via MCP
- **Parameter Handling**: String parameters correctly convert to typed parameters
- **Error Responses**: Exceptions properly formatted as MCP responses
- **Decorator Integration**: All decorators work together correctly
- **Edge Cases**: Invalid inputs, boundary conditions, error scenarios

#### Example Integration Test

```python
async def test_echo_tool_execution(self):
    """Test echo_tool works via MCP client."""
    session, cleanup = await create_test_session()
    try:
        result = await session.call_tool(
            "echo_tool",
            arguments={"message": "Hello MCP"}
        )
        assert "Hello MCP" in self._extract_text_content(result)
    finally:
        await cleanup()
```

## Coverage Configuration

### Subprocess Coverage Tracking

Integration tests spawn the MCP server as a subprocess, requiring special configuration to track coverage:

1. **`.coveragerc`**: Configures coverage for parallel/subprocess execution
2. **`sitecustomize.py`**: Automatically starts coverage in subprocesses
3. **`conftest.py`**: Sets the `COVERAGE_PROCESS_START` environment variable

### Current Coverage Targets

- **Overall**: ~40-45% (includes UI components which aren't tested)
- **Core Components**:
  - `example_tools.py`: 98% (all tools and edge cases)
  - `decorators/`: 80-100% per decorator
  - `server/app.py`: 82% (main entry point)
  - `config.py`: 80% (configuration management)

## Adding Tests for New Tools

When you add a new MCP tool to your server, follow these steps:

### 1. Add Unit Tests

Create unit tests for your tool's core logic:

```python
# tests/unit/test_my_tool.py
import pytest
from my_mcp_server.tools.my_tools import my_new_tool

def test_my_new_tool_success():
    """Test successful execution."""
    result = my_new_tool(param1="value1", param2=42)
    assert result["status"] == "success"
    assert result["data"] == expected_value

def test_my_new_tool_validation():
    """Test parameter validation."""
    with pytest.raises(ValueError):
        my_new_tool(param1="invalid", param2=-1)
```

### 2. Add Integration Tests

Add integration tests to verify MCP protocol compatibility:

```python
# tests/integration/test_my_tools.py
import pytest
from tests.integration.test_example_tools_integration import create_test_session

class TestMyTools:
    async def test_my_new_tool_via_mcp(self):
        """Test tool works via MCP protocol."""
        session, cleanup = await create_test_session()
        try:
            result = await session.call_tool(
                "my_new_tool",
                arguments={"param1": "value1", "param2": "42"}
            )
            # Verify result
            assert not result.isError
            # Extract and check content
        finally:
            await cleanup()
```

### 3. Add Edge Case Tests

Test error conditions and edge cases:

```python
async def test_my_new_tool_invalid_params(self):
    """Test tool handles invalid parameters."""
    session, cleanup = await create_test_session()
    try:
        result = await session.call_tool(
            "my_new_tool",
            arguments={"param1": "invalid"}  # Missing required param2
        )
        # Should handle the error gracefully
        error_msg = self._extract_error_message(result)
        assert "missing required" in error_msg.lower()
    finally:
        await cleanup()
```

## Important Notes

### Decorator Order

When tools are registered, decorators are applied in this order:
1. `exception_handler` (outermost - catches all exceptions)
2. `tool_logger` (logs execution details)
3. `parallelize` (for parallel tools only - innermost)

### Parallel Tools

Tools decorated with `@parallelize` have a different signature:
- Original: `async def my_tool(param1: str, param2: int) -> dict`
- After decoration: Expects `kwargs_list` parameter containing list of argument dictionaries

### Error Pattern

The `exception_handler` decorator returns structured errors instead of raising:
- Successful responses: `isError=False` with result data
- Caught exceptions: `isError=False` with error details in structured format
- This allows graceful error handling without breaking the MCP protocol

## Troubleshooting

### Low Coverage in Integration Tests

If integration tests show 0% or very low coverage:

1. **Check environment variable**:
   ```bash
   echo $COVERAGE_PROCESS_START  # Should show .coveragerc path
   ```

2. **Verify sitecustomize.py is loaded**:
   ```bash
   python -c "import sitecustomize; print('Loaded')"
   ```

3. **Check for coverage data files**:
   ```bash
   ls -la .coverage.*  # Should see files after test run
   ```

4. **Combine coverage data**:
   ```bash
   coverage combine  # Merges subprocess coverage data
   ```

### Test Failures

Common causes and solutions:

1. **Import errors**: Ensure you're in the project virtual environment
2. **Async issues**: Use `pytest.mark.anyio` for integration tests
3. **Cleanup errors**: Always use try/finally for session cleanup
4. **Parameter type issues**: Remember MCP passes strings, tools expect typed values

## Best Practices

1. **Test Isolation**: Each test should be independent and not rely on others
2. **Cleanup**: Always clean up resources (sessions, files, connections)
3. **Assertions**: Be specific in assertions - check exact values, not just truthy
4. **Edge Cases**: Test boundary conditions, empty inputs, invalid types
5. **Documentation**: Comment complex test logic and explain what's being tested
6. **Coverage**: Aim for high coverage on business logic, don't obsess over 100%

## Continuous Integration

For CI/CD pipelines, use:

```bash
# Run tests with coverage and fail if below threshold
uv run pytest tests/ --cov=my_mcp_server --cov-fail-under=40

# Generate coverage report for CI artifacts
uv run pytest tests/ --cov=my_mcp_server --cov-report=xml
```

## Contributing

When contributing new features:

1. Write unit tests for new functions/classes
2. Write integration tests for new MCP tools
3. Ensure all tests pass: `uv run pytest tests/`
4. Check coverage hasn't decreased: `uv run pytest tests/ --cov=my_mcp_server`
5. Update this documentation if you add new test patterns