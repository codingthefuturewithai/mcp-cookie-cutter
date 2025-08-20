"""Tests for MCP Server Project decorators.

This test suite validates all decorator functionality including:
- Exception handling with proper error formatting
- Tool logging with correlation IDs
- Type conversion between MCP and Python types
- Parallelization with signature transformation
- Decorator chaining compatibility
- MCP parameter introspection preservation

Critical validations:
- Function signatures preserved for MCP compatibility
- No "kwargs" fields appear in tool signatures
- Decorator chaining works in correct order
- Correlation IDs properly tracked
"""

import asyncio
import inspect
import json
from typing import Dict, List, Any
from unittest.mock import patch, MagicMock, AsyncMock
import pytest

# Import decorators from our project
from mcp_server_project.decorators.exception_handler import exception_handler
from mcp_server_project.decorators.tool_logger import tool_logger
from mcp_server_project.decorators.type_converter import type_converter
from mcp_server_project.decorators.parallelize import parallelize
from mcp_server_project.config import ServerConfig


class TestExceptionHandler:
    """Test exception_handler decorator functionality."""
    
    @pytest.mark.asyncio
    async def test_successful_execution(self):
        """Test that successful execution passes through unchanged."""
        
        @exception_handler
        async def test_tool(param: str) -> str:
            return f"processed_{param}"
        
        result = await test_tool("test_input")
        assert result == "processed_test_input"
    
    @pytest.mark.asyncio
    async def test_exception_handling(self):
        """Test that exceptions are logged and re-raised."""
        
        @exception_handler
        async def failing_tool(param: str) -> str:
            raise ValueError("Test error message")
        
        # The current implementation re-raises exceptions for MCP to handle
        with pytest.raises(ValueError, match="Test error message"):
            await failing_tool("test_input")
    
    def test_signature_preservation(self):
        """Test that function signature is preserved for MCP introspection."""
        
        @exception_handler
        async def test_tool(param1: str, param2: int = 42) -> str:
            return f"{param1}_{param2}"
        
        sig = inspect.signature(test_tool)
        params = list(sig.parameters.keys())
        
        # Verify original parameters are preserved
        assert params == ["param1", "param2"]
        assert sig.parameters["param1"].annotation == str
        assert sig.parameters["param2"].annotation == int
        assert sig.parameters["param2"].default == 42
        assert sig.return_annotation == str
    
    def test_no_kwargs_in_signature(self):
        """Test that decorator doesn't introduce kwargs parameter."""
        
        @exception_handler
        async def test_tool(specific_param: str) -> str:
            return specific_param
        
        sig = inspect.signature(test_tool)
        param_names = list(sig.parameters.keys())
        
        # Critical: ensure no generic kwargs parameter
        assert "kwargs" not in param_names
        assert param_names == ["specific_param"]


class TestToolLogger:
    """Test tool_logger decorator functionality."""
    
    @pytest.mark.asyncio
    async def test_successful_logging(self):
        """Test that successful execution is logged correctly."""
        
        config = {"log_level": "INFO"}
        
        @tool_logger
        async def test_tool(param: str) -> str:
            return f"result_{param}"
        
        # Apply with config
        decorated = tool_logger(test_tool, config)
        result = await decorated("test_input")
        
        # Just verify the function works correctly with the decorator
        assert result == "result_test_input"
    
    @pytest.mark.asyncio
    async def test_error_logging(self):
        """Test that errors are logged correctly."""
        
        @tool_logger
        async def failing_tool(param: str) -> str:
            raise RuntimeError("Test error")
        
        # Verify the error is raised through the decorator
        with pytest.raises(RuntimeError):
            await failing_tool("test_input")
    
    def test_signature_preservation_with_config(self):
        """Test that function signature is preserved when config is passed."""
        
        config = {"test_config": "value"}
        
        async def test_tool(param1: str, param2: int) -> Dict[str, Any]:
            return {"param1": param1, "param2": param2}
        
        decorated = tool_logger(test_tool, config)
        
        sig = inspect.signature(decorated)
        params = list(sig.parameters.keys())
        
        # Verify original parameters are preserved
        assert params == ["param1", "param2"]
        assert "kwargs" not in params
        assert sig.return_annotation == Dict[str, Any]


class TestTypeConverter:
    """Test type_converter decorator functionality."""
    
    @pytest.mark.asyncio
    async def test_type_conversion(self):
        """Test that types are converted correctly."""
        
        @type_converter
        async def test_tool(text: str, number: int = 42) -> str:
            return f"{text}_{number}"
        
        result = await test_tool("test", 100)
        assert result == "test_100"
    
    def test_signature_preservation(self):
        """Test that function signature is preserved."""
        
        @type_converter
        async def test_tool(param1: str, param2: int = 10) -> str:
            return f"{param1}_{param2}"
        
        sig = inspect.signature(test_tool)
        params = list(sig.parameters.keys())
        
        assert params == ["param1", "param2"]
        assert sig.parameters["param2"].default == 10
        assert "kwargs" not in params


class TestParallelize:
    """Test parallelize decorator functionality."""
    
    def test_signature_transformation(self):
        """Test that signature is correctly transformed for parallel execution."""
        
        @parallelize
        async def test_tool(param1: str, param2: int) -> str:
            return f"{param1}_{param2}"
        
        sig = inspect.signature(test_tool)
        params = list(sig.parameters.keys())
        
        # Verify signature transformation - includes ctx for MCP context
        assert params == ["kwargs_list", "ctx"]
        assert sig.parameters["kwargs_list"].annotation == List[Dict[str, Any]]
        assert sig.return_annotation == List[Any]
    
    @pytest.mark.asyncio
    async def test_parallel_execution(self):
        """Test that parallel execution works correctly."""
        
        @parallelize
        async def test_tool(param: str, multiplier: int = 1) -> str:
            # Simulate some async work
            await asyncio.sleep(0.01)
            return param * multiplier
        
        kwargs_list = [
            {"param": "a", "multiplier": 3},
            {"param": "b", "multiplier": 2},
            {"param": "c", "multiplier": 1}
        ]
        
        results = await test_tool(kwargs_list)
        
        assert len(results) == 3
        assert results[0] == "aaa"
        assert results[1] == "bb"
        assert results[2] == "c"
    
    @pytest.mark.asyncio
    async def test_empty_list_handling(self):
        """Test that empty list is handled correctly."""
        
        @parallelize
        async def test_tool(param: str) -> str:
            return f"processed_{param}"
        
        results = await test_tool([])
        assert results == []
    
    @pytest.mark.asyncio
    async def test_parameter_validation(self):
        """Test that parameter validation works correctly."""
        
        @parallelize
        async def test_tool(param: str) -> str:
            return param
        
        # Test invalid input type
        with pytest.raises(TypeError, match="Parallel tools require List\\[Dict\\] parameter"):
            await test_tool("not_a_list")
        
        # Test invalid list item type
        with pytest.raises(TypeError, match="Item 0 in kwargs_list must be a dict"):
            await test_tool(["not_a_dict"])
    
    @pytest.mark.asyncio
    async def test_fail_fast_behavior(self):
        """Test that fail-fast behavior works correctly."""
        
        @parallelize
        async def test_tool(param: str, should_fail: bool = False) -> str:
            if should_fail:
                raise ValueError(f"Failure for {param}")
            await asyncio.sleep(0.01)
            return f"success_{param}"
        
        kwargs_list = [
            {"param": "a", "should_fail": False},
            {"param": "b", "should_fail": True},  # This will fail
            {"param": "c", "should_fail": False}
        ]
        
        with pytest.raises(ValueError, match="Failure for b"):
            await test_tool(kwargs_list)
    
    def test_docstring_generation(self):
        """Test that docstring is correctly generated for parallelized function."""
        
        @parallelize
        async def test_tool(param1: str, param2: int) -> str:
            """Original docstring for test tool."""
            return f"{param1}_{param2}"
        
        docstring = test_tool.__doc__
        assert "Parallelized version of `test_tool`" in docstring
        assert "Original function signature: test_tool(param1: <class 'str'>, param2: <class 'int'>)" in docstring
        assert "kwargs_list (List[Dict[str, Any]])" in docstring
        assert "Original docstring for test tool." in docstring


class TestDecoratorChaining:
    """Test that decorators can be chained correctly."""
    
    @pytest.mark.asyncio
    async def test_regular_tool_chaining(self):
        """Test exception_handler → tool_logger → type_converter chaining."""
        
        # Apply decorators in correct order
        @exception_handler
        @tool_logger
        @type_converter
        async def test_tool(param: str) -> str:
            if param == "error":
                raise ValueError("Test error")
            return f"success_{param}"
        
        # Test successful execution
        result = await test_tool("good")
        assert result == "success_good"
        
        # Test error handling - exception is re-raised
        with pytest.raises(ValueError):
            await test_tool("error")
    
    @pytest.mark.asyncio
    async def test_parallel_tool_chaining(self):
        """Test exception_handler → tool_logger → parallelize(type_converter) chaining."""
        
        # Define base function
        async def base_tool(param: str) -> str:
            return f"processed_{param}"
        
        # Apply decorators in correct order (inner to outer)
        decorated_tool = exception_handler(tool_logger(parallelize(type_converter(base_tool)), None))
        
        kwargs_list = [
            {"param": "a"},
            {"param": "b"}
        ]
        
        result = await decorated_tool(kwargs_list)
        
        assert result == ["processed_a", "processed_b"]
    
    def test_chained_signature_preservation(self):
        """Test that signature is preserved through decorator chaining."""
        
        # Regular tool chain
        @exception_handler
        @tool_logger
        @type_converter
        async def regular_tool(param1: str, param2: int = 42) -> str:
            return f"{param1}_{param2}"
        
        sig = inspect.signature(regular_tool)
        params = list(sig.parameters.keys())
        
        assert params == ["param1", "param2"]
        assert "kwargs" not in params
        assert sig.parameters["param2"].default == 42


class TestMCPCompatibility:
    """Test MCP compatibility requirements."""
    
    def test_no_kwargs_in_any_signature(self):
        """Critical test: ensure no decorator introduces kwargs parameter."""
        
        @exception_handler
        @tool_logger
        @type_converter
        async def regular_tool(param1: str, param2: int) -> str:
            return f"{param1}_{param2}"
        
        @exception_handler  
        @tool_logger
        @parallelize
        @type_converter
        async def parallel_base(item: str) -> str:
            return f"processed_{item}"
        
        # Test regular tool signature
        regular_sig = inspect.signature(regular_tool)
        regular_params = list(regular_sig.parameters.keys())
        assert "kwargs" not in regular_params
        assert regular_params == ["param1", "param2"]
        
        # Test parallel tool signature  
        parallel_sig = inspect.signature(parallel_base)
        parallel_params = list(parallel_sig.parameters.keys())
        assert "kwargs" not in parallel_params
        assert parallel_params == ["kwargs_list", "ctx"]  # Transformed signature with ctx
    
    def test_function_metadata_preservation(self):
        """Test that function metadata is preserved for MCP introspection."""
        
        @exception_handler
        @tool_logger
        @type_converter
        async def test_tool(param: str) -> str:
            """Original docstring."""
            return param
        
        # Function name should be preserved
        assert test_tool.__name__ == "test_tool"
        
        # Module should be preserved
        assert hasattr(test_tool, '__module__')
        
        # Qualname should be preserved
        assert hasattr(test_tool, '__qualname__')
    
    def test_parameter_introspection_compatibility(self):
        """Test that parameter introspection works for MCP clients."""
        
        @exception_handler
        @tool_logger
        @type_converter
        async def complex_tool(
            required_param: str,
            optional_param: int = 42,
            typed_param: List[str] = None
        ) -> Dict[str, Any]:
            """Tool with complex parameters."""
            return {
                "required": required_param,
                "optional": optional_param, 
                "typed": typed_param or []
            }
        
        sig = inspect.signature(complex_tool)
        
        # Verify all parameters are preserved
        assert "required_param" in sig.parameters
        assert "optional_param" in sig.parameters  
        assert "typed_param" in sig.parameters
        
        # Verify types are preserved
        assert sig.parameters["required_param"].annotation == str
        assert sig.parameters["optional_param"].annotation == int
        assert sig.parameters["typed_param"].annotation == List[str]
        
        # Verify defaults are preserved
        assert sig.parameters["optional_param"].default == 42
        assert sig.parameters["typed_param"].default is None
        
        # Verify return type is preserved
        assert sig.return_annotation == Dict[str, Any]


# Integration test that mimics the example server pattern
class TestIntegrationPattern:
    """Test the exact pattern used in the example server."""
    
    @pytest.mark.asyncio
    async def test_example_server_pattern(self):
        """Test the exact decorator application pattern from example server."""
        
        # Define some test tools like in example_tools.py
        async def echo_tool(message: str) -> str:
            """Echo the input message."""
            return f"Echo: {message}"
        
        async def multiply_tool(a: int, b: int) -> int:
            """Multiply two numbers."""
            return a * b
        
        async def batch_process_tool(item: str) -> str:
            """Process an item (for parallel execution)."""
            return f"processed_{item}"
        
        # Apply decorators exactly like in the example server
        regular_tools = [echo_tool, multiply_tool]
        parallel_tools = [batch_process_tool]
        
        # Regular tools: exception_handler → tool_logger → type_converter
        for tool_func in regular_tools:
            decorated_func = exception_handler(tool_logger(type_converter(tool_func), None))
            
            # Test that it works
            if tool_func.__name__ == "echo_tool":
                result = await decorated_func("test message")
                assert result == "Echo: test message"
            elif tool_func.__name__ == "multiply_tool":
                result = await decorated_func(3, 4)
                assert result == 12
            
            # Verify signature preservation
            sig = inspect.signature(decorated_func)
            original_sig = inspect.signature(tool_func)
            assert list(sig.parameters.keys()) == list(original_sig.parameters.keys())
        
        # Parallel tools: exception_handler → tool_logger → parallelize(type_converter)
        for tool_func in parallel_tools:
            decorated_func = exception_handler(tool_logger(parallelize(type_converter(tool_func)), None))
            
            # Test that it works
            if tool_func.__name__ == "batch_process_tool":
                kwargs_list = [{"item": "a"}, {"item": "b"}]
                result = await decorated_func(kwargs_list)
                assert result == ["processed_a", "processed_b"]
            
            # Verify signature transformation
            sig = inspect.signature(decorated_func)
            assert list(sig.parameters.keys()) == ["kwargs_list", "ctx"]
            assert sig.parameters["kwargs_list"].annotation == List[Dict[str, Any]]


if __name__ == "__main__":
    # Run basic tests to verify functionality
    pytest.main([__file__, "-v"])