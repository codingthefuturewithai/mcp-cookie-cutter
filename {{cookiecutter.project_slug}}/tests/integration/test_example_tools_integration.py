"""MCP Client Integration Tests.

This test suite validates MCP tools work correctly when accessed via the actual
MCP client, testing the complete protocol flow including:
- Tool discovery and registration
- Parameter serialization (string → typed conversion)
- Error response formatting
- Decorator integration
- Real client-server interaction
- Multiple transport protocols (STDIO and Streamable HTTP)

These tests complement the unit tests by validating the full MCP protocol flow
rather than testing decorators in isolation. Tests are automatically run with
both STDIO and Streamable HTTP transports via the mcp_session fixture.
"""

import asyncio
import json
from typing import Optional, Dict, Any, List
import pytest
from mcp import types
from .conftest import extract_text_content, extract_error_text


# Use anyio instead of pytest-asyncio to match SDK approach
pytestmark = pytest.mark.anyio


class TestMCPToolDiscovery:
    """Test MCP tool discovery functionality."""
    
    async def test_all_tools_discoverable(self, mcp_session):
        """Test that all expected tools are discoverable via list_tools().
        
        This test runs with both STDIO and Streamable HTTP transports.
        """
        session, transport = mcp_session
        tools_response = await session.list_tools()
        
        # Extract tool names
        tool_names = [tool.name for tool in tools_response.tools]
        
        # Verify expected tools exist
        expected_tools = [
            "echo", # From echo.py
            "echo_tool", 
            "get_time", 
            "random_number", 
            "calculate_fibonacci",
            "search_tool",
            "elicit_example",
            "notification_example",
            "progress_example",
            "process_batch_data", 
            "simulate_heavy_computation"
        ]
        
        for expected in expected_tools:
            assert expected in tool_names, f"Tool {expected} not found in {tool_names} (transport: {transport})"
    
    async def test_no_kwargs_in_tool_schemas(self, mcp_session):
        """Test that no tool has a 'kwargs' parameter (MCP compatibility).
        
        This test runs with both STDIO and Streamable HTTP transports.
        """
        session, transport = mcp_session
        tools_response = await session.list_tools()
        
        for tool in tools_response.tools:
            if tool.inputSchema:
                properties = tool.inputSchema.get("properties", {})
                assert "kwargs" not in properties, (
                    f"Tool {tool.name} has kwargs parameter which breaks MCP compatibility (transport: {transport})"
                )
    
    async def test_tool_metadata_present(self, mcp_session):
        """Test that tools have proper metadata (description, schema).
        
        This test runs with both STDIO and Streamable HTTP transports.
        """
        session, transport = mcp_session
        tools_response = await session.list_tools()
        
        for tool in tools_response.tools:
            # Every tool should have a description
            assert tool.description, f"Tool {tool.name} missing description"
            
            # Tools should have input schemas
            assert tool.inputSchema is not None, f"Tool {tool.name} missing input schema"
            assert tool.inputSchema.get("type") == "object", (
                f"Tool {tool.name} schema type should be 'object' (transport: {transport})"
            )


class TestMCPToolExecution:
    """Test MCP tool execution with various parameter scenarios."""
    
    async def test_echo_tool_execution(self, mcp_session):
        """Test echo_tool works correctly via MCP client.
        
        This test runs with both STDIO and Streamable HTTP transports.
        """
        session, transport = mcp_session
        # Call tool with string parameter (as MCP sends)
        result = await session.call_tool("echo_tool", {"message": "Hello MCP World"})
        
        # Check result structure
        assert not result.isError, f"Tool execution failed: {result}"
        assert len(result.content) > 0, "No content returned"
        
        # Parse text content
        text_content = extract_text_content(result)
        assert text_content is not None, f"No text content found (transport: {transport})"
        assert "Hello MCP World" in text_content, f"Expected message not in response: {text_content} (transport: {transport})"
    
    async def test_echo_with_transform(self, mcp_session):
        """Test echo tool with case transformation.
        
        This test runs with both STDIO and Streamable HTTP transports.
        """
        session, transport = mcp_session
        
        # Test upper transformation
        result = await session.call_tool("echo", {"text": "hello", "transform": "upper"})
        assert not result.isError, f"Tool execution failed: {result}"
        text_content = extract_text_content(result)
        assert text_content == "HELLO", f"Expected HELLO, got {text_content} (transport: {transport})"
        
        # Test lower transformation
        result = await session.call_tool("echo", {"text": "WORLD", "transform": "lower"})
        assert not result.isError, f"Tool execution failed: {result}"
        text_content = extract_text_content(result)
        assert text_content == "world", f"Expected world, got {text_content} (transport: {transport})"
    
    async def test_get_time_execution(self, mcp_session):
        """Test get_time tool execution.
        
        This test runs with both STDIO and Streamable HTTP transports.
        """
        session, transport = mcp_session
        result = await session.call_tool("get_time", {})
        
        assert not result.isError, f"Tool execution failed: {result}"
        
        text_content = extract_text_content(result)
        assert text_content is not None, f"No text content found (transport: {transport})"
        
        # Should contain time-related text
        assert any(keyword in text_content.lower() for keyword in ["time", ":", "am", "pm", "utc"]), (
            f"Response doesn't appear to contain time: {text_content} (transport: {transport})"
        )
    
    async def test_random_number_with_defaults(self, mcp_session):
        """Test random_number tool with default parameters.
        
        This test runs with both STDIO and Streamable HTTP transports.
        """
        session, transport = mcp_session
        result = await session.call_tool("random_number", {})
        
        assert not result.isError, f"Tool execution failed: {result}"
        
        text_content = extract_text_content(result)
        # Try to parse the response as JSON (tools return structured data)
        try:
            data = json.loads(text_content)
            assert "number" in data, f"Response missing 'number' field: {data} (transport: {transport})"
            assert isinstance(data["number"], int), f"Number should be int: {data['number']} (transport: {transport})"
            assert 1 <= data["number"] <= 100, f"Number out of default range: {data['number']} (transport: {transport})"
        except (json.JSONDecodeError, ValueError):
            # If not JSON, try to extract number directly
            pytest.fail(f"Could not parse response as JSON: {text_content} (transport: {transport})")
    
    async def test_random_number_parameter_conversion(self, mcp_session):
        """Test string parameter conversion (MCP sends all params as strings).
        
        This test runs with both STDIO and Streamable HTTP transports.
        """
        session, transport = mcp_session
        # MCP protocol sends all parameters as strings
        result = await session.call_tool("random_number", {
            "min_value": "10",
            "max_value": "20"
        })
        
        assert not result.isError, f"Tool should handle string-to-int conversion (transport: {transport})"
        
        text_content = extract_text_content(result)
        try:
            data = json.loads(text_content)
            number = data["number"]
            assert 10 <= number <= 20, f"Number {number} out of specified range [10, 20] (transport: {transport})"
        except (json.JSONDecodeError, KeyError, ValueError) as e:
            pytest.fail(f"Failed to parse response: {e}, content: {text_content} (transport: {transport})")
    
    async def test_calculate_fibonacci_execution(self, mcp_session):
        """Test calculate_fibonacci with various inputs.
        
        This test runs with both STDIO and Streamable HTTP transports.
        """
        session, transport = mcp_session
        # Test with a reasonable value
        result = await session.call_tool("calculate_fibonacci", {"n": "10"})
        
        assert not result.isError, f"Tool execution failed: {result}"
        
        text_content = extract_text_content(result)
        try:
            data = json.loads(text_content)
            assert data["position"] == 10, f"Wrong position: {data} (transport: {transport})"
            assert data["value"] == 55, f"Wrong Fibonacci value for n=10: {data} (transport: {transport})"
        except (json.JSONDecodeError, KeyError) as e:
            pytest.fail(f"Failed to parse response: {e}, content: {text_content} (transport: {transport})")
    
    async def test_search_tool_execution(self, mcp_session):
        """Test search_tool with various parameter combinations.
        
        This test runs with both STDIO and Streamable HTTP transports.
        """
        session, transport = mcp_session
        
        # Test with required parameter only
        result = await session.call_tool("search_tool", {"query": "test search"})
        assert not result.isError, f"Tool execution failed: {result}"
        
        text_content = extract_text_content(result)
        try:
            data = json.loads(text_content)
            assert data["query"] == "test search", f"Query not preserved: {data} (transport: {transport})"
            assert "results" in data, f"No results field in response: {data} (transport: {transport})"
            assert isinstance(data["results"], list), f"Results should be a list: {data} (transport: {transport})"
        except (json.JSONDecodeError, KeyError) as e:
            pytest.fail(f"Failed to parse response: {e}, content: {text_content} (transport: {transport})")
    
    async def test_search_tool_with_optional_params(self, mcp_session):
        """Test search_tool with optional parameters.
        
        This test runs with both STDIO and Streamable HTTP transports.
        """
        session, transport = mcp_session
        
        # Test with all optional parameters
        result = await session.call_tool("search_tool", {
            "query": "advanced search",
            "max_results": "3",
            "directories": ["dir1", "dir2"],
            "include_hidden": "true"
        })
        
        assert not result.isError, f"Tool execution failed: {result}"
        
        text_content = extract_text_content(result)
        try:
            data = json.loads(text_content)
            assert data["query"] == "advanced search", f"Query not preserved: {data} (transport: {transport})"
            assert data["max_results"] == 3, f"Max results not converted: {data} (transport: {transport})"
            assert data["directories"] == ["dir1", "dir2"], f"Directories not preserved: {data} (transport: {transport})"
            assert data["include_hidden"] == True, f"Include hidden not converted: {data} (transport: {transport})"
            assert len(data["results"]) <= 3, f"Too many results returned: {data} (transport: {transport})"
        except (json.JSONDecodeError, KeyError) as e:
            pytest.fail(f"Failed to parse response: {e}, content: {text_content} (transport: {transport})")
    
    async def test_elicit_example_with_available_date(self, mcp_session):
        """Test elicit_example tool with an available date.
        
        This test runs with both STDIO and Streamable HTTP transports.
        """
        session, transport = mcp_session
        
        # Test with available date (not 2024-12-25)
        result = await session.call_tool("elicit_example", {
            "date": "2024-12-26",
            "time": "19:00",
            "party_size": "4"
        })
        
        assert not result.isError, f"Tool execution failed: {result}"
        
        text_content = extract_text_content(result)
        assert "[SUCCESS] Booked for 2024-12-26 at 19:00" in text_content, (
            f"Expected success message not found: {text_content} (transport: {transport})"
        )
    
    async def test_notification_example_execution(self, mcp_session):
        """Test notification_example tool with logging capabilities.
        
        This test runs with both STDIO and Streamable HTTP transports.
        """
        session, transport = mcp_session
        
        result = await session.call_tool("notification_example", {
            "data": "test data for processing"
        })
        
        assert not result.isError, f"Tool execution failed: {result}"
        
        text_content = extract_text_content(result)
        assert "Processed: test data for processing" in text_content, (
            f"Expected processed message not found: {text_content} (transport: {transport})"
        )
    
    async def test_progress_example_execution(self, mcp_session):
        """Test progress_example tool with progress updates.
        
        This test runs with both STDIO and Streamable HTTP transports.
        """
        session, transport = mcp_session
        
        # Test with default steps
        result = await session.call_tool("progress_example", {
            "task_name": "Test Task"
        })
        
        assert not result.isError, f"Tool execution failed: {result}"
        
        text_content = extract_text_content(result)
        assert "Task 'Test Task' completed" in text_content, (
            f"Expected completion message not found: {text_content} (transport: {transport})"
        )
    
    async def test_progress_example_with_custom_steps(self, mcp_session):
        """Test progress_example tool with custom step count.
        
        This test runs with both STDIO and Streamable HTTP transports.
        """
        session, transport = mcp_session
        
        # Test with custom steps
        result = await session.call_tool("progress_example", {
            "task_name": "Custom Task",
            "steps": "3"
        })
        
        assert not result.isError, f"Tool execution failed: {result}"
        
        text_content = extract_text_content(result)
        assert "Task 'Custom Task' completed" in text_content, (
            f"Expected completion message not found: {text_content} (transport: {transport})"
        )
    
    async def test_process_batch_data_parallel_execution(self, mcp_session):
        """Test process_batch_data parallel tool execution.
        
        This test runs with both STDIO and Streamable HTTP transports.
        """
        session, transport = mcp_session
        # Parallel tools expect a specific format
        kwargs_list = [
            {"items": ["hello", "world"], "operation": "upper"},
            {"items": ["foo", "bar"], "operation": "lower"},
            {"items": ["test"], "operation": "reverse"}
        ]
        
        result = await session.call_tool("process_batch_data", {
            "kwargs_list": kwargs_list
        })
        
        assert not result.isError, f"Tool execution failed: {result}"
        
        # Parallel tools return a list of results
        text_content = extract_text_content(result)
        try:
            results = json.loads(text_content)
            assert isinstance(results, list), f"Expected list of results, got {type(results)} (transport: {transport})"
            assert len(results) == 3, f"Expected 3 results, got {len(results)} (transport: {transport})"
            
            # Verify each result
            assert results[0]["processed"] == ["HELLO", "WORLD"]
            assert results[1]["processed"] == ["foo", "bar"]
            assert results[2]["processed"] == ["tset"]
        except (json.JSONDecodeError, KeyError) as e:
            pytest.fail(f"Failed to parse response: {e}, content: {text_content} (transport: {transport})")
    
    async def test_simulate_heavy_computation_execution(self, mcp_session):
        """Test simulate_heavy_computation parallel tool.
        
        This test runs with both STDIO and Streamable HTTP transports.
        """
        session, transport = mcp_session
        kwargs_list = [
            {"complexity": "3"},
            {"complexity": "5"}
        ]
        
        result = await session.call_tool("simulate_heavy_computation", {
            "kwargs_list": kwargs_list
        })
        
        assert not result.isError, f"Tool execution failed: {result}"
        
        text_content = extract_text_content(result)
        try:
            results = json.loads(text_content)
            assert isinstance(results, list), f"Expected list of results, got {type(results)} (transport: {transport})"
            assert len(results) == 2, f"Expected 2 results, got {len(results)} (transport: {transport})"
            
            # Check that results have expected structure
            for i, res in enumerate(results):
                assert "complexity" in res, f"Result {i} missing complexity (transport: {transport})"
                assert "iterations" in res, f"Result {i} missing iterations (transport: {transport})"
                assert "result" in res, f"Result {i} missing result (transport: {transport})"
                assert "computation_time" in res, f"Result {i} missing computation_time (transport: {transport})"
        except (json.JSONDecodeError, KeyError) as e:
            pytest.fail(f"Failed to parse response: {e}, content: {text_content} (transport: {transport})")


class TestMCPErrorHandling:
    """Test MCP error handling scenarios."""
    
    async def test_missing_required_parameter(self, mcp_session):
        """Test error handling when required parameter is missing.
        
        This test runs with both STDIO and Streamable HTTP transports.
        """
        session, transport = mcp_session
        # Call echo_tool without required 'message' parameter
        result = await session.call_tool("echo_tool", {})
        
        # Should return error
        assert result.isError, "Should return error for missing required parameter"
        
        # Check error content
        error_text = extract_error_text(result)
        assert error_text, f"No error text found (transport: {transport})"
        assert any(keyword in error_text.lower() for keyword in ["error", "missing", "required"]), (
            f"Error message doesn't indicate missing parameter: {error_text} (transport: {transport})"
        )
    
    async def test_invalid_parameter_type(self, mcp_session):
        """Test error handling with invalid parameter types.
        
        This test runs with both STDIO and Streamable HTTP transports.
        """
        session, transport = mcp_session
        # Send invalid type that can't be converted
        result = await session.call_tool("calculate_fibonacci", {
            "n": "not_a_number"
        })
        
        assert result.isError, "Should return error for invalid parameter type"
        
        error_text = extract_error_text(result)
        assert error_text, f"No error text found (transport: {transport})"
        assert any(keyword in error_text.lower() for keyword in ["error", "invalid", "type", "int"]), (
            f"Error message doesn't indicate type error: {error_text} (transport: {transport})"
        )
    
    async def test_tool_exception_handling(self, mcp_session):
        """Test error format when tool raises exception.
        
        This test runs with both STDIO and Streamable HTTP transports.
        """
        session, transport = mcp_session
        # Negative Fibonacci should raise an error
        result = await session.call_tool("calculate_fibonacci", {"n": "-1"})
        
        # May or may not be marked as error depending on exception handling
        text_content = extract_text_content(result) or extract_error_text(result)
        assert text_content, f"No content found in response (transport: {transport})"
        
        # Check for error indication
        assert any(keyword in text_content.lower() for keyword in ["error", "negative", "invalid", "non-negative"]), (
            f"Response doesn't indicate error: {text_content} (transport: {transport})"
        )
    
    async def test_nonexistent_tool(self, mcp_session):
        """Test error when calling non-existent tool.
        
        This test runs with both STDIO and Streamable HTTP transports.
        """
        session, transport = mcp_session
        result = await session.call_tool("nonexistent_tool", {"param": "value"})
        
        assert result.isError, "Should return error for non-existent tool"
        
        error_text = extract_error_text(result)
        assert error_text, f"No error text found (transport: {transport})"
        assert any(keyword in error_text.lower() for keyword in ["not found", "unknown", "invalid"]), (
            f"Error doesn't indicate unknown tool: {error_text} (transport: {transport})"
        )
    
    async def test_parallel_tool_invalid_format(self, mcp_session):
        """Test error handling for parallel tools with invalid input format.
        
        This test runs with both STDIO and Streamable HTTP transports.
        """
        session, transport = mcp_session
        # Send non-list to parallel tool
        result = await session.call_tool("process_batch_data", {
            "kwargs_list": "not_a_list"
        })
        
        assert result.isError, "Should return error for invalid parallel tool input"
        
        error_text = extract_error_text(result)
        assert error_text, f"No error text found (transport: {transport})"
        assert any(keyword in error_text.lower() for keyword in ["list", "type", "error"]), (
            f"Error doesn't indicate type issue: {error_text} (transport: {transport})"
        )


class TestMCPProtocolCompliance:
    """Test MCP protocol compliance and edge cases."""
    
    async def test_multiple_tools_in_sequence(self, mcp_session):
        """Test calling multiple tools in sequence.
        
        This test runs with both STDIO and Streamable HTTP transports.
        """
        session, transport = mcp_session
        # Call multiple tools to ensure session remains stable
        tools_to_test = [
            ("get_time", {}),
            ("echo_tool", {"message": "test"}),
            ("random_number", {"min_value": "1", "max_value": "10"}),
            ("search_tool", {"query": "sequential test"}),
            ("notification_example", {"data": "sequential data"}),
            ("progress_example", {"task_name": "Sequential Task"}),
        ]
        
        for tool_name, params in tools_to_test:
            result = await session.call_tool(tool_name, params)
            assert not result.isError, f"Tool {tool_name} failed: {result} (transport: {transport})"
            assert len(result.content) > 0, f"Tool {tool_name} returned no content (transport: {transport})"
    
    async def test_concurrent_tool_calls(self, mcp_session):
        """Test that tools handle concurrent calls correctly.
        
        This test runs with both STDIO and Streamable HTTP transports.
        """
        session, transport = mcp_session
        # Create multiple concurrent tool calls
        tasks = [
            session.call_tool("random_number", {"min_value": "1", "max_value": "100"}),
            session.call_tool("echo_tool", {"message": "concurrent test"}),
            session.call_tool("get_time", {}),
            session.call_tool("search_tool", {"query": "concurrent search"}),
            session.call_tool("notification_example", {"data": "concurrent data"}),
        ]
        
        # Execute concurrently
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Verify all succeeded
        for i, result in enumerate(results):
            assert not isinstance(result, Exception), f"Task {i} raised exception: {result} (transport: {transport})"
            assert not result.isError, f"Task {i} returned error: {result} (transport: {transport})"
    
    async def test_large_parameter_handling(self, mcp_session):
        """Test handling of large parameters.
        
        This test runs with both STDIO and Streamable HTTP transports.
        """
        session, transport = mcp_session
        # Create a large message
        large_message = "x" * 10000  # 10KB message
        
        result = await session.call_tool("echo_tool", {"message": large_message})
        
        assert not result.isError, f"Failed with large parameter: {result} (transport: {transport})"
        
        text_content = extract_text_content(result)
        assert large_message in text_content, f"Large message not properly echoed (transport: {transport})"


# Test runner for direct execution
if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])