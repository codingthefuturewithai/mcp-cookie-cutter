"""
REFERENCE PATTERNS FOR MCP INTEGRATION TESTS - DO NOT DELETE

This file contains canonical patterns for testing MCP tools using the MCP client.
These tests validate the complete protocol flow including parameter conversion,
error handling, and decorator behavior.

CRITICAL UNDERSTANDING:
- Integration tests use a real MCP client session
- They test the COMPLETE flow: client → server → decorators → tool → response
- The session.call_tool() method sends actual MCP protocol messages
- Error handling behavior depends on decorator implementation
"""

import json
import pytest
from mcp import types
from typing import Optional, Dict, Any, List


# ============================================================================
# TEST SESSION CREATION PATTERN (ALWAYS USE THIS)
# ============================================================================
async def create_test_session():
    """
    Creates an MCP client session for testing.
    
    THIS IS THE CANONICAL PATTERN - Always use this exact approach:
    1. Creates stdio client connection to your MCP server
    2. Returns (session, cleanup) tuple
    3. ALWAYS call cleanup() in finally block
    
    Returns:
        Tuple of (session, cleanup_function)
    """
    import sys
    import os
    from pathlib import Path
    from mcp import ClientSession, StdioServerParameters
    from mcp.client.stdio import stdio_client, get_default_environment
    
    # Get project root and server module
    project_root = Path(__file__).parent.parent.parent
    server_module = f"mcp_server_project.server.app"
    
    # Build environment with proper Python path
    env = get_default_environment()
    env["PYTHONPATH"] = str(project_root)
    
    # Create server parameters
    server_params = StdioServerParameters(
        command=sys.executable,
        args=["-m", server_module],
        env=env
    )
    
    # Start stdio client (CORRECT PATTERN - must use async with)
    # Note: This helper does manual context management for compatibility
    stdio_context = stdio_client(server_params)
    read, write = await stdio_context.__aenter__()
    
    # Create and initialize session
    session = ClientSession(read, write)
    await session.__aenter__()
    await session.initialize()
    
    # Define cleanup function
    async def cleanup():
        try:
            await session.__aexit__(None, None, None)
        except Exception:
            pass
        try:
            await stdio_context.__aexit__(None, None, None)
        except Exception:
            pass
    
    return session, cleanup


# ============================================================================
# PATTERN 1: Testing Successful Tool Execution
# ============================================================================
@pytest.mark.anyio  # Use anyio marker for async tests
async def test_successful_tool_execution_pattern():
    """
    PATTERN: Testing a tool that executes successfully.
    
    Key points:
    - Use create_test_session() to get MCP client
    - Call tool with session.call_tool()
    - Check result.isError is False for success
    - Extract text content from result
    - ALWAYS cleanup in finally block
    """
    # Step 1: Create test session
    session, cleanup = await create_test_session()
    try:
        # Step 2: Call the tool with parameters
        result = await session.call_tool(
            "tool_name",  # Tool name as registered in server
            arguments={    # Arguments as dictionary
                "param1": "value1",
                "param2": 42
            }
        )
        
        # Step 3: Verify successful execution
        assert result.isError is False, f"Tool failed: {result}"
        
        # Step 4: Extract and verify content
        text_content = None
        for content in result.content:
            if isinstance(content, types.TextContent):
                text_content = content.text
                break
        
        assert text_content is not None, "No text content in response"
        
        # Step 5: Parse and verify response (tools often return JSON)
        try:
            data = json.loads(text_content)
            assert "expected_field" in data
            assert data["expected_field"] == "expected_value"
        except json.JSONDecodeError:
            # If not JSON, verify text content directly
            assert "expected text" in text_content
            
    finally:
        # Step 6: ALWAYS cleanup
        await cleanup()


# ============================================================================
# PATTERN 2: Testing Error Handling
# ============================================================================
@pytest.mark.anyio
async def test_error_handling_pattern():
    """
    PATTERN: Testing tool error handling.
    
    CRITICAL: With the current decorator implementation:
    - Exceptions are RE-RAISED by @exception_handler
    - This means result.isError will be True
    - Error message can be extracted from result.content
    """
    session, cleanup = await create_test_session()
    try:
        # Call tool with invalid parameters that will cause an error
        result = await session.call_tool(
            "tool_name",
            arguments={
                "min_value": 100,  # Invalid: min > max
                "max_value": 10
            }
        )
        
        # IMPORTANT: Exception is re-raised, so isError is True
        assert result.isError is True, "Should return error for invalid input"
        
        # Extract error message
        error_msg = ""
        for content in result.content:
            if isinstance(content, types.TextContent):
                error_msg = content.text
                break
        
        # Verify error message contains expected text
        assert "min_value must be less than or equal to max_value" in error_msg
        
    finally:
        await cleanup()


# ============================================================================
# PATTERN 3: Testing Parameter Type Conversion
# ============================================================================
@pytest.mark.anyio
async def test_parameter_conversion_pattern():
    """
    PATTERN: Testing MCP's string-to-type parameter conversion.
    
    Key points:
    - MCP sends ALL parameters as strings
    - The type_converter decorator converts them to correct types
    - Test with string values to ensure conversion works
    """
    session, cleanup = await create_test_session()
    try:
        # Send parameters as strings (how MCP actually sends them)
        result = await session.call_tool(
            "calculate_something",
            arguments={
                "number_param": "42",      # String, will convert to int
                "float_param": "3.14",     # String, will convert to float
                "bool_param": "true",      # String, will convert to bool
                "list_param": '["a","b"]'  # JSON string, will convert to list
            }
        )
        
        assert result.isError is False
        
        # Verify the tool received and processed correct types
        text_content = _extract_text_content(result)
        data = json.loads(text_content)
        
        # Tool should have received proper types after conversion
        assert data["received_int"] == 42
        assert data["received_float"] == 3.14
        assert data["received_bool"] is True
        assert data["received_list"] == ["a", "b"]
        
    finally:
        await cleanup()


# ============================================================================
# PATTERN 4: Testing Parallel Tools
# ============================================================================
@pytest.mark.anyio
async def test_parallel_tool_pattern():
    """
    PATTERN: Testing tools decorated with @parallelize.
    
    Key points:
    - Parallel tools expect 'kwargs_list' parameter
    - kwargs_list is a list of dictionaries
    - Each dict contains parameters for one execution
    - Results come back as multiple TextContent items
    """
    session, cleanup = await create_test_session()
    try:
        # Prepare batch of work items
        kwargs_list = [
            {"item": "first", "operation": "upper"},
            {"item": "second", "operation": "lower"},
            {"item": "third", "operation": "reverse"}
        ]
        
        # Call parallel tool
        result = await session.call_tool(
            "batch_process_tool",
            arguments={
                "kwargs_list": kwargs_list  # Single parameter with list
            }
        )
        
        assert result.isError is False
        
        # Extract all results (one per work item)
        results = []
        for content in result.content:
            if isinstance(content, types.TextContent):
                try:
                    results.append(json.loads(content.text))
                except json.JSONDecodeError:
                    results.append(content.text)
        
        # Verify we got results for all items
        assert len(results) == len(kwargs_list)
        
        # Verify each result
        assert results[0]["processed"] == "FIRST"
        assert results[1]["processed"] == "second"
        assert results[2]["processed"] == "driht"
        
    finally:
        await cleanup()


# ============================================================================
# PATTERN 5: Testing Missing Required Parameters
# ============================================================================
@pytest.mark.anyio
async def test_missing_parameter_pattern():
    """
    PATTERN: Testing behavior when required parameters are missing.
    
    The MCP server should return an error when required parameters are missing.
    """
    session, cleanup = await create_test_session()
    try:
        # Call tool without required parameter
        result = await session.call_tool(
            "echo_tool",
            arguments={}  # Missing required 'message' parameter
        )
        
        # Should return error
        assert result.isError is True
        
        # Verify error message mentions missing parameter
        error_text = _extract_error_text(result)
        assert any(word in error_text.lower() 
                  for word in ["missing", "required", "parameter"])
        
    finally:
        await cleanup()


# ============================================================================
# PATTERN 6: Testing Edge Cases
# ============================================================================
@pytest.mark.anyio
async def test_edge_cases_pattern():
    """
    PATTERN: Testing edge cases and boundary conditions.
    
    Always test:
    - Empty inputs
    - Null/None values
    - Maximum/minimum values
    - Invalid types
    - Special characters
    """
    session, cleanup = await create_test_session()
    try:
        # Test 1: Empty string
        result = await session.call_tool(
            "echo_tool",
            arguments={"message": ""}
        )
        assert result.isError is False
        
        # Test 2: Very long input
        long_message = "x" * 10000
        result = await session.call_tool(
            "echo_tool",
            arguments={"message": long_message}
        )
        assert result.isError is False
        text = _extract_text_content(result)
        assert long_message in text
        
        # Test 3: Special characters
        special_chars = "!@#$%^&*()[]{}|\\<>?,./~`"
        result = await session.call_tool(
            "echo_tool",
            arguments={"message": special_chars}
        )
        assert result.isError is False
        
    finally:
        await cleanup()


# ============================================================================
# HELPER FUNCTIONS (Use these in your tests)
# ============================================================================

def _extract_text_content(result: types.CallToolResult) -> Optional[str]:
    """
    Helper to extract text content from MCP result.
    
    Use this pattern in your tests to get the actual response text.
    """
    for content in result.content:
        if isinstance(content, types.TextContent):
            return content.text
    return None


def _extract_error_text(result: types.CallToolResult) -> Optional[str]:
    """
    Helper to extract error text from MCP error result.
    
    Use this when result.isError is True.
    """
    if result.isError and result.content:
        return _extract_text_content(result)
    return None


def _parse_json_response(result: types.CallToolResult) -> Optional[Dict[str, Any]]:
    """
    Helper to parse JSON response from tool.
    
    Many tools return JSON-formatted strings.
    """
    text = _extract_text_content(result)
    if text:
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            return None
    return None


# ============================================================================
# TEST CLASS ORGANIZATION PATTERN
# ============================================================================

class TestYourToolIntegration:
    """
    PATTERN: Organize related tests in classes.
    
    Benefits:
    - Logical grouping of related tests
    - Shared fixtures within class
    - Clear test organization
    """
    
    def _extract_text_content(self, result):
        """Shared helper method."""
        for content in result.content:
            if isinstance(content, types.TextContent):
                return content.text
        return None
    
    @pytest.mark.anyio
    async def test_your_tool_success(self):
        """Test successful execution."""
        session, cleanup = await create_test_session()
        try:
            result = await session.call_tool(
                "your_tool",
                arguments={"param": "value"}
            )
            assert result.isError is False
            # More assertions...
        finally:
            await cleanup()
    
    @pytest.mark.anyio
    async def test_your_tool_error(self):
        """Test error handling."""
        session, cleanup = await create_test_session()
        try:
            result = await session.call_tool(
                "your_tool",
                arguments={"invalid": "params"}
            )
            assert result.isError is True
            # More assertions...
        finally:
            await cleanup()


# ============================================================================
# CRITICAL TEST PATTERNS TO REMEMBER
# ============================================================================

"""
ALTERNATE PATTERN (If create_test_session doesn't work):

If you encounter issues with the create_test_session() helper, you can use
the direct async context manager pattern:

async def test_with_direct_pattern():
    from mcp.client.stdio import stdio_client
    
    async with stdio_client.stdio_server(
        command="python",
        args=["-m", "server.app"],
        env={"PYTHONPATH": "."}
    ) as (read_stream, write_stream):
        async with stdio_client.StdioServerSession(read_stream, write_stream) as session:
            result = await session.call_tool("tool_name", arguments={})
            assert result.isError is False

UNDERSTANDING result.isError:

1. When result.isError is False:
   - Tool executed successfully
   - Response is in result.content as TextContent
   - Extract with _extract_text_content()

2. When result.isError is True:
   - Tool raised an exception OR
   - MCP validation failed (missing params, wrong types)
   - Error message is in result.content
   - Extract with _extract_error_text()

DECORATOR BEHAVIOR IN TESTS:

With current implementation:
- @exception_handler RE-RAISES exceptions
- This means errors result in isError = True
- Test assertions should expect:
  - Success: assert result.isError is False
  - Error: assert result.isError is True

COMMON TEST MISTAKES TO AVOID:

1. ❌ Forgetting cleanup:
   session, cleanup = await create_test_session()
   result = await session.call_tool(...)  # No finally block!
   
   ✅ Always use try/finally:
   session, cleanup = await create_test_session()
   try:
       result = await session.call_tool(...)
   finally:
       await cleanup()

2. ❌ Not checking isError:
   result = await session.call_tool(...)
   data = json.loads(result.content[0].text)  # May crash!
   
   ✅ Always check isError first:
   result = await session.call_tool(...)
   assert result.isError is False
   text = _extract_text_content(result)

3. ❌ Assuming response format:
   text = result.content[0].text  # Assumes content[0] exists and is text
   
   ✅ Use helper functions:
   text = _extract_text_content(result)
   if text:
       # Process text

4. ❌ Not testing error cases:
   # Only testing happy path
   
   ✅ Always test both success and error cases:
   - Valid inputs
   - Invalid inputs
   - Missing parameters
   - Edge cases
"""