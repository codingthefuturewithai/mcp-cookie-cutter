# Coverage Testing for MCP Integration Tests

## Overview

Integration tests spawn the MCP server as a subprocess, which requires special configuration to track code execution in the subprocess. This guide explains how our coverage tracking works and how to troubleshoot issues.

## How Subprocess Coverage Works

### The Challenge
When integration tests launch the MCP server as a subprocess (exactly as a real MCP client would), normal coverage tracking doesn't capture code execution in that subprocess.

### The Solution
We use a three-part solution to enable subprocess coverage tracking:

1. **`.coveragerc`** - Configuration file that enables parallel coverage mode
2. **`sitecustomize.py`** - Python startup hook that initializes coverage in subprocesses
3. **Environment variables** - Pass coverage settings to the subprocess

## Configuration Details

### 1. `.coveragerc` Configuration

```ini
[run]
source = my_mcp_server
parallel = true                    # Enable parallel/subprocess tracking
concurrency = multiprocessing       # Support multiprocessing
data_file = .coverage              # Base coverage data file
omit = 
    */site-packages/*              # Exclude third-party packages
    */dist-packages/*
    */.venv/*
    */venv/*
    */tests/*
    */__pycache__/*
    /opt/*
    /usr/*

[report]
exclude_lines =
    pragma: no cover
    def __repr__
    if self\.debug
    raise AssertionError
    raise NotImplementedError
    if __name__ == .__main__.:
```

### 2. `sitecustomize.py` Implementation

This file is automatically imported by Python on startup when it's in the Python path:

```python
"""Enable coverage measurement in subprocesses."""
import os

# Only run coverage if COVERAGE_PROCESS_START is set
if os.environ.get('COVERAGE_PROCESS_START'):
    import coverage
    import atexit
    import signal
    import sys
    
    # Start coverage immediately before any other imports
    cov = coverage.Coverage(config_file=os.environ.get('COVERAGE_PROCESS_START'))
    cov.start()
    
    # Save for later access
    import builtins
    builtins._coverage_instance = cov
    
    def save_coverage_data(signum=None, frame=None):
        """Save coverage data when process is terminated."""
        try:
            if hasattr(builtins, '_coverage_instance'):
                c = builtins._coverage_instance
                c.stop()
                c.save()
        except Exception:
            pass
        
        # Exit cleanly on signal
        if signum is not None:
            sys.exit(0)
    
    # Register handlers for saving coverage data
    atexit.register(save_coverage_data)
    signal.signal(signal.SIGTERM, save_coverage_data)
    signal.signal(signal.SIGINT, save_coverage_data)
```

### 3. Environment Variable Passing

The integration tests pass coverage environment variables to the subprocess:

```python
# From test_example_tools_integration.py
async def create_test_session():
    # Build environment with coverage tracking support
    env = get_default_environment()  # Get MCP SDK's safe defaults
    
    # Add coverage-related environment variables if they exist
    coverage_vars = [
        "COVERAGE_PROCESS_START",
        "COVERAGE_FILE",
        "COVERAGE_CORE",
        "COV_CORE_SOURCE",
        "COV_CORE_CONFIG",
        "COV_CORE_DATAFILE",
    ]
    
    for var in coverage_vars:
        if var in os.environ:
            env[var] = os.environ[var]
    
    # Add PYTHONPATH to ensure sitecustomize.py can be found
    env["PYTHONPATH"] = str(project_root)
```

## Running Tests with Coverage

### Standard Test Run with Coverage

```bash
# Run all tests with coverage
uv run pytest tests/ --cov=my_mcp_server --cov-report=term --cov-report=html

# Run only integration tests with coverage
uv run pytest tests/integration/ --cov=my_mcp_server --cov-report=term
```

### Manual Coverage Workflow

If you need more control:

```bash
# 1. Set the environment variable
export COVERAGE_PROCESS_START=.coveragerc

# 2. Clear any previous coverage data
coverage erase

# 3. Run the tests
coverage run -m pytest tests/integration/

# 4. Combine parallel coverage data files
coverage combine

# 5. Generate report
coverage report
coverage html
```

## Understanding Coverage Output

### Expected Coverage Levels

- **Overall**: ~40-45% (includes untested UI components)
- **example_tools.py**: 98% (comprehensive tool testing)
- **decorators/**: 80-100% (decorator functionality)
- **server/app.py**: 82% (main entry point, SSE transport not tested)
- **config.py**: 80% (configuration management)

### Why Some Lines Aren't Covered

1. **UI Components** (`ui/` directory): Not tested (0% coverage) as they require Streamlit
2. **SSE Transport**: Some transport-specific lines may not be tested
3. **Error Recovery**: Some error paths may not be reachable in tests
4. **Main Block**: `if __name__ == "__main__"` blocks aren't executed during imports

Note: Integration tests now support both STDIO and Streamable HTTP transports via parameterized fixtures, providing better coverage across transport types.

## Troubleshooting

### Problem: 0% Coverage in Integration Tests

**Symptom**: Integration tests pass but show 0% coverage for subprocess code.

**Solutions**:

1. **Check environment variable is set**:
   ```bash
   # In conftest.py, this should be set automatically
   echo $COVERAGE_PROCESS_START  # Should show .coveragerc
   ```

2. **Verify sitecustomize.py is being loaded**:
   ```bash
   python -c "import sitecustomize; print('Coverage tracking enabled')"
   ```

3. **Check for parallel coverage data files**:
   ```bash
   # After running tests, you should see multiple coverage files
   ls -la .coverage.*
   ```

4. **Manually combine coverage data**:
   ```bash
   coverage combine
   coverage report
   ```

### Problem: Coverage Lower Than Expected

**Possible Causes**:

1. **Tests failing early**: Failed tests may not save coverage data properly
2. **Missing edge cases**: Add tests for error conditions and boundary cases
3. **Dead code**: Some code paths may be unreachable
4. **Conditional code**: Code behind feature flags or platform checks

**Solutions**:

1. Run tests individually to identify failures
2. Add edge case tests (see `test_example_tools_edge_cases.py`)
3. Review HTML coverage report to identify missing lines
4. Consider if low-coverage code is actually needed

### Problem: Coverage Not Tracking Third-Party Packages

**This is intentional!** The `.coveragerc` file excludes third-party packages to focus on your code.

## Tips for Improving Coverage

1. **Test Error Paths**: Don't just test success cases
   ```python
   # Test invalid parameters
   result = await session.call_tool("tool", {"invalid": "params"})
   assert "error" in result.lower()
   ```

2. **Test Edge Cases**: Boundary conditions often reveal bugs
   ```python
   # Test with minimum/maximum values
   result = await session.call_tool("fibonacci", {"n": 0})
   result = await session.call_tool("fibonacci", {"n": 100})
   ```

3. **Test All Tool Variations**: Each tool should have multiple test cases
   ```python
   # Test with different parameter combinations
   # Test with missing optional parameters
   # Test with invalid types
   ```

4. **Use Coverage Reports**: The HTML report shows exactly which lines aren't covered
   ```bash
   coverage html
   open htmlcov/index.html  # Review line-by-line coverage
   ```

## Advanced Topics

### Branch Coverage

For more thorough testing, enable branch coverage:

```bash
# Run with branch coverage
coverage run --branch -m pytest tests/
coverage report --show-missing
```

### Coverage in CI/CD

For continuous integration:

```bash
# Generate XML report for CI tools
coverage xml

# Fail if coverage drops below threshold
pytest tests/ --cov=my_mcp_server --cov-fail-under=40
```

### Debugging Coverage Issues

Enable coverage debugging:

```bash
# Set debug mode
export COVERAGE_DEBUG=trace

# Run tests - will show detailed coverage operations
pytest tests/integration/ -v
```

## Summary

The subprocess coverage tracking system ensures that integration tests properly measure code coverage even when the MCP server runs as a separate process. This gives us confidence that our tests are actually exercising the code paths we think they are, and helps identify areas that need more testing.