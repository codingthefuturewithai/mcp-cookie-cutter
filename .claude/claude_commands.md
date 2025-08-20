# Claude Commands for MCP Cookie Cutter

This file contains custom Claude commands for working with the MCP Cookie Cutter template.

## Getting Started

**Command**: Generate MCP Server

**Description**: Create a new MCP server project from the cookie cutter template with all features enabled.

**Instructions**:
```bash
# Generate a new MCP server project with all features
cookiecutter . --no-input \
  project_name="My MCP Server" \
  project_slug="my_mcp_server" \
  author_name="Developer" \
  author_email="dev@example.com" \
  project_description="A comprehensive MCP server with all features"

# The post-generation hook will automatically:
# - Create virtual environment
# - Install dependencies with uv sync
# - Install UI dependencies with uv sync --extra ui
# - Set up the project structure
```

## Add Tools

**Command**: Add New Tool to MCP Server

**Description**: Add a new tool to an existing MCP server project following the established patterns.

**Instructions**:
1. Create a new tool file in `{{project_slug}}/tools/`:
```python
# {{project_slug}}/tools/my_new_tool.py
import logging
from typing import Dict, Any
from mcp.server.fastmcp import Context

logger = logging.getLogger(__name__)

async def my_new_tool(
    param1: str,
    param2: int = 10,
    ctx: Context = None
) -> Dict[str, Any]:
    """
    Description of what your tool does.
    
    Args:
        param1: First parameter description
        param2: Optional second parameter (default: 10)
        ctx: MCP Context for advanced features
    
    Returns:
        Dictionary with tool results
    """
    logger.info(f"Executing my_new_tool with param1={param1}, param2={param2}")
    
    # Your tool logic here
    result = process_data(param1, param2)
    
    return {
        "input": param1,
        "multiplier": param2,
        "result": result,
        "status": "success"
    }
```

2. Register the tool in `{{project_slug}}/server/app.py`:
```python
from {{project_slug}}.tools.my_new_tool import my_new_tool

# Add to the appropriate tools list
example_tools = [
    # ... existing tools
    my_new_tool,  # Add your new tool here
]
```

3. Add tests for your tool in `tests/integration/`:
```python
# tests/integration/test_my_new_tool.py
import pytest
from mcp_client_test_utils import create_test_session

@pytest.mark.asyncio
async def test_my_new_tool():
    session, cleanup = await create_test_session()
    try:
        result = await session.call_tool(
            "my_new_tool",
            arguments={"param1": "test", "param2": 5}
        )
        assert result.isError is False
        # Add more assertions
    finally:
        await cleanup()
```

## Generate Test

**Command**: Generate Integration Test for Tool

**Description**: Create a comprehensive integration test for an MCP tool following the established testing patterns.

**Instructions**:
```python
# tests/integration/test_{{tool_name}}_integration.py
"""
Integration tests for {{tool_name}} tool.

Tests the complete MCP protocol flow including:
- Parameter conversion
- Decorator behavior
- Error handling
- Response formatting
"""

import json
import pytest
from typing import Optional
from mcp import types
from pathlib import Path
import sys

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from tests.integration.conftest import create_test_session


class Test{{ToolName}}Integration:
    """Integration tests for {{tool_name}} tool."""
    
    @staticmethod
    def _extract_text_content(result: types.CallToolResult) -> Optional[str]:
        """Extract text content from MCP result."""
        for content in result.content:
            if isinstance(content, types.TextContent):
                return content.text
        return None
    
    @pytest.mark.asyncio
    async def test_{{tool_name}}_success(self):
        """Test successful execution of {{tool_name}}."""
        session, cleanup = await create_test_session()
        try:
            # Call the tool with valid parameters
            result = await session.call_tool(
                "{{tool_name}}",
                arguments={
                    "param1": "test_value",
                    "param2": 42
                }
            )
            
            # Verify successful execution
            assert result.isError is False, f"Tool failed: {result}"
            
            # Extract and verify response
            text_content = self._extract_text_content(result)
            assert text_content is not None, "No text content in response"
            
            # Parse JSON response (if applicable)
            data = json.loads(text_content)
            assert "expected_field" in data
            assert data["status"] == "success"
            
        finally:
            await cleanup()
    
    @pytest.mark.asyncio
    async def test_{{tool_name}}_error_handling(self):
        """Test error handling for {{tool_name}}."""
        session, cleanup = await create_test_session()
        try:
            # Call with invalid parameters
            result = await session.call_tool(
                "{{tool_name}}",
                arguments={
                    "invalid_param": "bad_value"
                }
            )
            
            # Should return error
            assert result.isError is True
            
            # Verify error message
            error_text = self._extract_text_content(result)
            assert "error" in error_text.lower()
            
        finally:
            await cleanup()
    
    @pytest.mark.asyncio
    async def test_{{tool_name}}_parameter_conversion(self):
        """Test parameter type conversion for {{tool_name}}."""
        session, cleanup = await create_test_session()
        try:
            # Send parameters as strings (MCP protocol behavior)
            result = await session.call_tool(
                "{{tool_name}}",
                arguments={
                    "number_param": "123",  # String -> int
                    "float_param": "3.14",  # String -> float
                    "bool_param": "true"    # String -> bool
                }
            )
            
            assert result.isError is False
            
            # Verify correct type conversion
            text_content = self._extract_text_content(result)
            data = json.loads(text_content)
            
            # Verify types were converted correctly
            assert isinstance(data["received_number"], int)
            assert isinstance(data["received_float"], float)
            assert isinstance(data["received_bool"], bool)
            
        finally:
            await cleanup()
    
    @pytest.mark.asyncio
    async def test_{{tool_name}}_edge_cases(self):
        """Test edge cases for {{tool_name}}."""
        session, cleanup = await create_test_session()
        try:
            # Test empty input
            result = await session.call_tool(
                "{{tool_name}}",
                arguments={"param": ""}
            )
            assert result.isError is False
            
            # Test very long input
            long_input = "x" * 10000
            result = await session.call_tool(
                "{{tool_name}}",
                arguments={"param": long_input}
            )
            assert result.isError is False
            
            # Test special characters
            special = "!@#$%^&*()[]{}|\\<>?,./~`"
            result = await session.call_tool(
                "{{tool_name}}",
                arguments={"param": special}
            )
            assert result.isError is False
            
        finally:
            await cleanup()


# Run with: pytest tests/integration/test_{{tool_name}}_integration.py -v
```

## Remove Example Tools

**Command**: Remove Example Tools from MCP Server

**Description**: Clean up the MCP server by removing all example tools, keeping only the core echo tool.

**Instructions**:
1. **Remove example tools file**:
```bash
rm {{project_slug}}/tools/example_tools.py
```

2. **Update server/app.py** to remove example tool registrations:
```python
# {{project_slug}}/server/app.py

# Remove these imports:
# from {{project_slug}}.tools.example_tools import (
#     echo_tool, get_time, random_number, ...
# )

# Keep only the basic echo tool:
from {{project_slug}}.tools.echo import echo

# In create_mcp_server():
# Remove the example_tools and parallel_example_tools lists
# Keep only:
@mcp.tool()
async def echo_handler(text: str, transform: Optional[str] = None) -> str:
    return await echo(text, transform)
```

3. **Remove example tool tests**:
```bash
rm tests/integration/test_example_tools_integration.py
rm tests/unit/test_example_tools.py
```

4. **Update imports in remaining files**:
- Check `{{project_slug}}/tools/__init__.py` and remove example tool exports
- Update any documentation that references example tools

5. **Verify the cleanup**:
```bash
# Check that server still starts
{{project_slug}}-server --help

# Test that echo still works
{{project_slug}}-client "Hello, World!"

# Run remaining tests
pytest tests/
```

## Usage

To use these commands in Claude:

1. **Getting Started**: Use when creating a new MCP server project
2. **Add Tools**: Use when adding new functionality to an existing server
3. **Generate Test**: Use when creating tests for new or existing tools
4. **Remove Example Tools**: Use when preparing a production server

Each command provides a complete workflow with code templates and verification steps.