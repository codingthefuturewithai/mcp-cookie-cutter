---
description: Generate comprehensive unit and integration tests for MCP tools by studying test patterns
argument-hint: "[tool-name-or-module]"
allowed-tools: ["Read", "Write", "Grep", "Glob", "Bash", "KillBash"]
---

# Generate Tests for Your MCP Tool

## 🚨 IMPORTANT: Environment Ready

**Virtual environment and dependencies already installed!**
- ✅ Test framework (pytest) ready to use
- ✅ Use `uv run pytest` for all test commands
- ⚠️ NEVER use global pip or pytest

## CRITICAL: Process Check First

**Before generating tests, we need a clean slate.**

Let me check if any MCP processes are running:

```bash
# Windows PowerShell:
Get-Process | Where-Object {$_.ProcessName -match "python|uv"} | Select-Object Id, ProcessName
# Mac/Linux:
ps aux | grep -E "mcp|uv run" | grep -v grep
```

If processes found: "I need to kill these processes before generating tests. The server must restart to test your new code."

```bash
# Kill any running processes
# Windows:
taskkill /PID <PID> /F
# Mac/Linux:
kill <PIDs>
```

**Why?** Tests need to import your latest tool code. Running processes lock the modules.

## Step 1: Study Test Patterns and Compatibility Rules

First, let me review the canonical test patterns AND compatibility requirements:

Reading .reference/patterns/integration_test_patterns.py for MCP client test patterns...
Reading .reference/patterns/unit_test_patterns.py for unit test patterns...
Reading .reference/mcp-compatibility-critical.md for MANDATORY compatibility rules...

**🚨 CRITICAL COMPATIBILITY RULE**:
- NEVER generate tests with Optional[...] parameters
- Use empty defaults instead (empty string, 0, empty list)
- This prevents MCP client failures

Key patterns I'll follow:
- Integration tests use `create_test_session()` for MCP client
- Always use try/finally with cleanup()
- Check `result.isError` based on expected behavior
- Test both success and error cases
- NO Optional types in test parameters

## Step 2: Analyze the Tool to Test

Looking for the tool: "$ARGUMENTS"

**MANDATORY CHECK - Verify NO Optional Parameters:**
```
Checking tool parameters...
❌ FAIL if ANY Optional[...] found
✅ PASS if all optional params use concrete defaults
```

Reading the tool implementation to understand:
- Parameters (NO Optional types allowed!)
- Return type
- Error conditions
- Validation logic
- Whether it's a parallel tool

## Step 3: Generate Integration Tests

Creating comprehensive integration tests following the pattern from .reference/patterns/integration_test_patterns.py:

### Test Cases to Generate:
1. **Successful execution** - Happy path with valid inputs
2. **Parameter conversion** - Test string-to-type conversion
3. **Error handling** - Invalid inputs that raise exceptions
4. **Missing parameters** - Required parameters not provided
5. **Edge cases** - Boundary conditions, empty inputs, etc.

### Critical Test Pattern:
```python
async def test_[tool_name]_[scenario]():
    session, cleanup = await create_test_session()
    try:
        # NEVER use Optional in test parameters!
        result = await session.call_tool("[tool_name]", arguments={
            "directories": [],  # NOT Optional[List[str]]
            "max_count": 10,    # NOT Optional[int]
            "filter": "",       # NOT Optional[str]
            "enabled": True     # NOT Optional[bool]
        })
        assert result.isError is False  # or True for errors
    finally:
        await cleanup()
```

## Step 4: Generate Unit Tests (if applicable)

If testing decorator behavior or specific functions:

Following patterns from .reference/patterns/unit_test_patterns.py:
- Test signature preservation
- Test decorator chaining
- Use mocks for external dependencies

## Step 5: Create Test Files

**🚨 CRITICAL: Always create NEW test files - NEVER modify existing test files!**

Creating YOUR test file(s):
- Integration: tests/integration/test_[your_tool_name].py  (NEW FILE)
- Unit (if needed): tests/unit/test_[your_tool_name].py  (NEW FILE)

**DO NOT modify these existing files:**
- test_example_tools_integration.py (example tests only)
- test_example_tools_edge_cases.py (example tests only)
- test_decorators.py (decorator infrastructure tests)

Your new test file should be completely independent.

Each test includes:
- Clear docstrings explaining what's being tested
- Proper assertions with helpful failure messages
- Coverage of success and failure paths

## Step 6: Test Execution Instructions

### Pre-Test Process Check

**IMPORTANT**: Before running tests, ensure no MCP processes are running:

```bash
# Check again for any lingering processes
# Windows PowerShell:
Get-Process | Where-Object {$_.ProcessName -match "python|uv"} | Select-Object Id, ProcessName
# Mac/Linux:
ps aux | grep -E "mcp|uv run" | grep -v grep
```

If any found, kill them before proceeding.

### Running Your Tests

**First, ensure your virtual environment is activated:**
```bash
# Windows PowerShell:
.venv\Scripts\Activate.ps1
# Windows CMD:
.venv\Scripts\activate.bat
# Mac/Linux:
source .venv/bin/activate
```

Now run your new tests:

```bash
# Run specific test file
uv run pytest tests/integration/test_[your_module].py -v

# Run with coverage
uv run pytest tests/integration/test_[your_module].py --cov=[module_name]

# Run specific test
uv run pytest tests/integration/test_[your_module].py::TestClassName::test_method_name
```

### Debug Support

**Tell me what happened:**
- ✅ "All tests passed!" → Excellent! Ready to integrate with AI
- ⚠️ "Some tests failed" → Share the failures, let's fix them
- ❌ "Import errors" → Likely process issue, let's restart

**Common Issues:**
1. **Import Error**: Old processes running → Kill and retry
2. **Test Failure**: Share the error → I'll help debug
3. **Connection Error**: MCP client issue → Check test setup

## Important Testing Notes

Based on the patterns in .reference/:
- When exceptions are raised in tools, `result.isError` will be `True`
- MCP sends all parameters as strings - test type conversion
- Parallel tools expect `kwargs_list` parameter
- Always extract content with helper methods, don't assume structure

## 🎉 SUCCESS: Tests Generated and Passing!

Your tool is now fully tested and production-ready! 

### Clean Up Example Code (Optional)

Now that you have YOUR working tools and tests, you can remove the example code:

```
/remove-examples
```

This will remove all 6 example tools and their tests, keeping YOUR code intact.

### Other Next Steps:

1. **Run full test suite**: `uv run pytest`
2. **Integration with AI**: Update Claude Desktop config  
3. **Create more tools**: Use `/add-tool` for next feature

Your tool is ready for production use in Claude Desktop or other MCP clients!