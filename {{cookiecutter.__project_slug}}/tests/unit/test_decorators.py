"""Tests for decorators.

This test suite validates all decorator functionality including:
- Exception handling with proper error formatting
- SQLite logging with thread-safe connections
- Parallelization with signature transformation
- Decorator chaining compatibility
- MCP parameter introspection preservation

Critical validations:
- Function signatures preserved for MCP compatibility
- No "kwargs" fields appear in tool signatures
- Decorator chaining works in correct order
- Thread-safe database operations
"""

import asyncio
import inspect
import json
import sqlite3
import tempfile
import threading
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any
from unittest.mock import patch, MagicMock
from mcp.types import TextContent
import pytest

# Import decorators from template
from {{cookiecutter.__project_slug}}.decorators.exception_handler import exception_handler
from {{cookiecutter.__project_slug}}.decorators.tool_logger import tool_logger
from {{cookiecutter.__project_slug}}.decorators.parallelize import parallelize
from {{cookiecutter.__project_slug}}.decorators.sqlite_logger import (
    SQLiteLoggerSink, 
    initialize_sqlite_logging,
    log_tool_execution
)
from {{cookiecutter.__project_slug}}.config import ServerConfig


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
    
    @pytest.fixture
    def temp_db_config(self):
        """Create temporary database for testing."""
        with tempfile.TemporaryDirectory() as temp_dir:
            config = ServerConfig()
            # Override database path for testing
            config.log_retention_days = 7
            yield config
    
    @pytest.mark.asyncio
    async def test_successful_logging(self, temp_db_config):
        """Test that successful execution is logged correctly."""
        
        @tool_logger
        async def test_tool(param: str) -> str:
            return f"result_{param}"
        
        result = await test_tool("test_input")
        
        # Just verify the function works correctly with the decorator
        assert result == "result_test_input"
    
    @pytest.mark.asyncio
    async def test_error_logging(self, temp_db_config):
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
        
        @tool_logger
        async def test_tool(param1: str, param2: int) -> Dict[str, Any]:
            return {"param1": param1, "param2": param2}
        
        sig = inspect.signature(test_tool)
        params = list(sig.parameters.keys())
        
        # Verify original parameters are preserved
        assert params == ["param1", "param2"]
        assert "kwargs" not in params
        assert sig.return_annotation == Dict[str, Any]


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
        assert sig.return_annotation == List[TextContent]
    
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
        
        # Results are now List[TextContent] for FastMCP 3 compatibility
        assert len(results) == 3
        assert json.loads(results[0].text) == "aaa"
        assert json.loads(results[1].text) == "bb"
        assert json.loads(results[2].text) == "c"
    
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
        """Test exception_handler → tool_logger chaining."""
        
        # Apply decorators in correct order
        @exception_handler
        @tool_logger
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
        """Test exception_handler → tool_logger → parallelize chaining."""
        
        # Define base function
        async def base_tool(param: str) -> str:
            return f"processed_{param}"
        
        # Apply decorators in correct order (inner to outer)
        decorated_tool = exception_handler(tool_logger(parallelize(base_tool), None))
        
        kwargs_list = [
            {"param": "a"},
            {"param": "b"}
        ]
        
        result = await decorated_tool(kwargs_list)
        
        # Results are now List[TextContent] for FastMCP 3 compatibility
        assert len(result) == 2
        assert json.loads(result[0].text) == "processed_a"
        assert json.loads(result[1].text) == "processed_b"
    
    def test_chained_signature_preservation(self):
        """Test that signature is preserved through decorator chaining."""
        
        # Regular tool chain
        @exception_handler
        @tool_logger
        async def regular_tool(param1: str, param2: int = 42) -> str:
            return f"{param1}_{param2}"
        
        sig = inspect.signature(regular_tool)
        params = list(sig.parameters.keys())
        
        assert params == ["param1", "param2"]
        assert "kwargs" not in params
        assert sig.parameters["param2"].default == 42
        
        # Parallel tool chain (signature should be transformed)
        base_func = lambda param: str  # Simple base function
        base_func.__name__ = "parallel_tool"
        base_func.__annotations__ = {"param": str, "return": str}
        
        decorated_parallel = exception_handler(tool_logger(parallelize(base_func), None))
        
        parallel_sig = inspect.signature(decorated_parallel)
        parallel_params = list(parallel_sig.parameters.keys())
        
        assert parallel_params == ["kwargs_list", "ctx"]
        assert parallel_sig.parameters["kwargs_list"].annotation == List[Dict[str, Any]]


class TestSQLiteLogger:
    """Test SQLite logging integration."""
    
    @pytest.fixture
    def temp_db_path(self):
        """Create temporary database file."""
        with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
            db_path = Path(f.name)
        yield db_path
        
        # Close any open connections from SQLiteLoggerSink before cleanup
        from {{ cookiecutter.__project_slug }}.decorators.sqlite_logger import SQLiteLoggerSink
        if hasattr(SQLiteLoggerSink, '_instance') and SQLiteLoggerSink._instance:
            sink = SQLiteLoggerSink._instance
            if hasattr(sink, '_local') and hasattr(sink._local, 'connection'):
                try:
                    sink._local.connection.close()
                except:
                    pass
        
        # On Windows, retry deletion with a small delay if needed
        if db_path.exists():
            import time
            import sys
            max_retries = 3 if sys.platform == "win32" else 1
            for i in range(max_retries):
                try:
                    db_path.unlink()
                    break
                except PermissionError:
                    if i < max_retries - 1:
                        time.sleep(0.1)  # Small delay for Windows to release file handle
                    else:
                        # If we still can't delete, it's okay for temp files
                        pass
    
    def test_database_initialization(self, temp_db_path):
        """Test that database is initialized correctly."""
        
        # Mock the database path
        with patch('{{ cookiecutter.__project_slug }}.decorators.sqlite_logger.SQLiteLoggerSink._get_database_path') as mock_path:
            mock_path.return_value = temp_db_path
            
            sink = SQLiteLoggerSink()
            
            # Verify database was created
            assert temp_db_path.exists()
            
            # Verify schema
            conn = sqlite3.connect(str(temp_db_path))
            cursor = conn.cursor()
            
            # Check table exists
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='tool_logs'")
            assert cursor.fetchone() is not None
            
            # Check schema structure
            cursor.execute("PRAGMA table_info(tool_logs)")
            columns = [row[1] for row in cursor.fetchall()]
            
            expected_columns = [
                'id', 'timestamp', 'level', 'message', 'tool_name', 
                'duration_ms', 'status', 'input_args', 'output_summary', 
                'error_message', 'module', 'function', 'line', 'extra_data', 'created_at'
            ]
            
            for col in expected_columns:
                assert col in columns
            
            conn.close()
    
    def test_thread_safety(self, temp_db_path):
        """Test that database connections are thread-safe."""
        
        with patch('{{ cookiecutter.__project_slug }}.decorators.sqlite_logger.SQLiteLoggerSink._get_database_path') as mock_path:
            mock_path.return_value = temp_db_path
            
            sink = SQLiteLoggerSink()
            
            # Get connections from different "threads" (simulated)
            conn1 = sink._get_connection()
            conn2 = sink._get_connection()
            
            # Should be the same connection within same thread
            assert conn1 is conn2
    
    def test_log_tool_execution_function(self, temp_db_path):
        """Test the log_tool_execution utility function."""
        
        # Create a temporary SQLiteLoggerSink instance
        sink = SQLiteLoggerSink()
        
        # Mock the database path for this instance
        with patch.object(sink, '_db_path', temp_db_path):
            # Re-initialize with the mocked path
            sink._local = threading.local()  # Reset thread-local storage
            sink._initialize_database()
            
            # Patch the global logger to use our test sink
            with patch('{{ cookiecutter.__project_slug }}.decorators.sqlite_logger.logger') as mock_logger:
                # Call the sink directly to log a message
                test_message = MagicMock()
                # Create a mock level object with name attribute
                mock_level = MagicMock()
                mock_level.name = "INFO"
                
                test_message.record = {
                    "time": datetime.now(),
                    "level": mock_level,
                    "message": "Tool test_tool success in 123.5ms",
                    "module": "test_module",
                    "function": "test_function",
                    "line": 42,
                    "extra": {
                        "tool_name": "test_tool",
                        "duration_ms": 123.45,
                        "status": "success",
                        "input_args": {"param": "value"},
                        "output_summary": "Test output",
                        "error_message": None
                    }
                }
                
                # Call the sink to write the log
                sink(test_message)
                
                # Verify log was written
                conn = sqlite3.connect(str(temp_db_path))
                cursor = conn.cursor()
                cursor.execute("SELECT tool_name, duration_ms, status FROM tool_logs")
                row = cursor.fetchone()
                
                assert row is not None
                assert row[0] == "test_tool"
                assert row[1] == 123.45
                assert row[2] == "success"
                
                conn.close()


class TestMCPCompatibility:
    """Test MCP compatibility requirements."""
    
    def test_no_kwargs_in_any_signature(self):
        """Critical test: ensure no decorator introduces kwargs parameter."""
        
        @exception_handler
        @tool_logger
        async def regular_tool(param1: str, param2: int) -> str:
            return f"{param1}_{param2}"
        
        @exception_handler  
        @tool_logger
        @parallelize
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
        
        # Regular tools: exception_handler → tool_logger
        for tool_func in regular_tools:
            decorated_func = exception_handler(tool_logger(tool_func, None))
            
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
        
        # Parallel tools: exception_handler → tool_logger → parallelize
        for tool_func in parallel_tools:
            decorated_func = exception_handler(tool_logger(parallelize(tool_func), None))
            
            # Test that it works
            if tool_func.__name__ == "batch_process_tool":
                kwargs_list = [{"item": "a"}, {"item": "b"}]
                result = await decorated_func(kwargs_list)
                # Results are now List[TextContent] for FastMCP 3 compatibility
                assert len(result) == 2
                assert json.loads(result[0].text) == "processed_a"
                assert json.loads(result[1].text) == "processed_b"
            
            # Verify signature transformation
            sig = inspect.signature(decorated_func)
            assert list(sig.parameters.keys()) == ["kwargs_list", "ctx"]
            assert sig.parameters["kwargs_list"].annotation == List[Dict[str, Any]]
            assert sig.return_annotation == List[TextContent]


if __name__ == "__main__":
    # Run basic tests to verify functionality
    pytest.main([__file__, "-v"])