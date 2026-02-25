"""
REFERENCE PATTERNS FOR MCP TOOLS - DO NOT DELETE

This file contains canonical patterns for creating MCP tools that work with
the MCP server decorator system. AI assistants use these patterns to generate
consistent, correct code.

CRITICAL RULES:
1. ALL tools must be async functions
2. ALL tools must accept ctx: Context = None as last parameter
3. ALL tools must have type hints for parameters and return values
4. ALL tools must have docstrings
5. NEVER use generic 'kwargs' parameter - always use specific parameter names
"""

from typing import Dict, List, Any, Optional
from fastmcp import Context


# ============================================================================
# PATTERN 1: Simple Tool with Single Parameter
# ============================================================================
async def simple_tool_pattern(message: str, ctx: Context = None) -> str:
    """
    PATTERN: Basic MCP tool with single required parameter.
    
    This pattern shows:
    - Async function declaration (REQUIRED)
    - Single typed parameter
    - Context parameter at the end (REQUIRED)
    - Simple string return type
    - Clear docstring
    
    Args:
        message: The input message to process
        ctx: MCP context (automatically provided by runtime, NEVER remove)
        
    Returns:
        Processed message as a string
    """
    # Tool implementation goes here
    return f"Processed: {message}"


# ============================================================================
# PATTERN 2: Tool with Optional Parameters and Defaults
# ============================================================================
async def tool_with_defaults_pattern(
    required_param: str,
    optional_int: int = 42,
    optional_bool: bool = False,
    ctx: Context = None
) -> Dict[str, Any]:
    """
    PATTERN: Tool with mix of required and optional parameters.
    
    This pattern shows:
    - Required parameters come first (no default value)
    - Optional parameters have default values
    - Multiple parameter types (str, int, bool)
    - Dictionary return type for structured data
    - Context ALWAYS comes last
    
    IMPORTANT: MCP sends all parameters as strings, but the type_converter
    decorator handles conversion automatically.
    
    Args:
        required_param: Required string parameter
        optional_int: Optional integer with default value
        optional_bool: Optional boolean flag
        ctx: MCP context (automatically provided)
        
    Returns:
        Dictionary with processed results
    """
    result = {
        "required": required_param,
        "int_value": optional_int,
        "flag": optional_bool,
        "processed_at": time.time()
    }
    return result


# ============================================================================
# PATTERN 3: Tool with Error Handling
# ============================================================================
async def tool_with_validation_pattern(
    min_value: int,
    max_value: int,
    ctx: Context = None
) -> Dict[str, Any]:
    """
    PATTERN: Tool with input validation and error handling.
    
    This pattern shows:
    - Input validation with clear error messages
    - Raising exceptions for invalid input
    - The exception_handler decorator will catch and format errors
    
    IMPORTANT: When exceptions are raised, they are re-raised by the
    exception_handler decorator for MCP to handle properly. This means
    test assertions should expect result.isError = True for errors.
    
    Args:
        min_value: Minimum value for range
        max_value: Maximum value for range
        ctx: MCP context
        
    Returns:
        Dictionary with validation results
        
    Raises:
        ValueError: If min_value > max_value
    """
    # Validation - raise clear exceptions
    if min_value > max_value:
        raise ValueError("min_value must be less than or equal to max_value")
    
    if min_value < 0:
        raise ValueError("min_value must be non-negative")
    
    # Process after validation
    return {
        "range": f"{min_value}-{max_value}",
        "valid": True
    }


# ============================================================================
# PATTERN 4: Tool with Complex Types
# ============================================================================
async def tool_with_complex_types_pattern(
    items: List[str],
    config: Optional[Dict[str, Any]] = None,
    ctx: Context = None
) -> List[Dict[str, Any]]:
    """
    PATTERN: Tool accepting complex types like lists and dictionaries.
    
    This pattern shows:
    - List parameter type
    - Optional dictionary parameter
    - Complex return type (list of dictionaries)
    - Handling None/empty inputs
    
    Args:
        items: List of items to process
        config: Optional configuration dictionary
        ctx: MCP context
        
    Returns:
        List of processed results
    """
    # Handle empty/None inputs gracefully
    if not items:
        return []
    
    config = config or {}  # Default to empty dict if None
    
    results = []
    for item in items:
        results.append({
            "original": item,
            "processed": item.upper() if config.get("uppercase", False) else item,
            "length": len(item)
        })
    
    return results


# ============================================================================
# PATTERN 5: Computationally Intensive Tool
# ============================================================================
async def computation_tool_pattern(
    n: int,
    ctx: Context = None
) -> Dict[str, Any]:
    """
    PATTERN: Tool that performs intensive computation.
    
    This pattern shows:
    - Time tracking for performance metrics
    - Async-friendly computation (with yields)
    - Detailed result metadata
    
    Args:
        n: Input parameter for computation
        ctx: MCP context
        
    Returns:
        Dictionary with computation results and metrics
    """
    import time
    import asyncio
    
    start_time = time.time()
    
    # Perform computation
    result = 0
    for i in range(n):
        result += i
        # Yield control periodically in async context
        if i % 1000 == 0:
            await asyncio.sleep(0)  # Let other tasks run
    
    computation_time = time.time() - start_time
    
    return {
        "input": n,
        "result": result,
        "computation_time_ms": computation_time * 1000,
        "operations": n
    }


# ============================================================================
# PATTERN 6: Tool for Parallel Execution
# ============================================================================
async def parallel_tool_base_pattern(
    item: str,
    operation: str = "upper",
    ctx: Context = None
) -> str:
    """
    PATTERN: Base tool designed for parallel execution.
    
    This pattern shows:
    - Simple signature (will be transformed by @parallelize)
    - Single item processing logic
    - The @parallelize decorator will transform this to accept
      kwargs_list: List[Dict[str, Any]] instead
    
    IMPORTANT: When @parallelize is applied:
    - Original signature: (item: str, operation: str = "upper")
    - Transformed signature: (kwargs_list: List[Dict[str, Any]], ctx: Context = None)
    - Each dict in kwargs_list contains: {"item": "...", "operation": "..."}
    
    Args:
        item: Single item to process
        operation: Operation to perform
        ctx: MCP context
        
    Returns:
        Processed item
    """
    # Process single item
    if operation == "upper":
        return item.upper()
    elif operation == "lower":
        return item.lower()
    elif operation == "reverse":
        return item[::-1]
    else:
        raise ValueError(f"Unknown operation: {operation}")


# ============================================================================
# CRITICAL PATTERNS TO UNDERSTAND
# ============================================================================

"""
DECORATOR APPLICATION PATTERNS:

1. REGULAR TOOLS (Most Common):
   @exception_handler  # Outer: Catches exceptions, re-raises for MCP
   @tool_logger       # Inner: Logs execution to SQLite
   async def my_tool(..., ctx: Context = None):
       pass

2. PARALLEL TOOLS (For Batch Processing):
   @exception_handler  # Outer: Catches exceptions
   @tool_logger       # Middle: Logs execution
   @parallelize       # Inner: Transforms signature for parallel execution
   async def my_batch_tool(..., ctx: Context = None):
       pass

WHAT DECORATORS DO:

1. @exception_handler:
   - Catches exceptions from the tool
   - RE-RAISES them (this is critical for tests!)
   - Preserves function signature for MCP introspection
   - This means: test assertions use result.isError = True for errors

2. @tool_logger:
   - Logs tool execution to SQLite database
   - Records: timestamp, duration, status, inputs, outputs, errors
   - Thread-safe database connections
   - Does NOT modify function signature

3. @parallelize:
   - TRANSFORMS function signature
   - Original: (param1: type1, param2: type2, ctx: Context = None)
   - Transformed: (kwargs_list: List[Dict[str, Any]], ctx: Context = None)
   - Executes tool in parallel for each dict in kwargs_list
   - Preserves parameter introspection for documentation

4. @type_converter:
   - Converts string parameters from MCP to correct Python types
   - Handles: int, float, bool, List, Dict, Optional types
   - Applied automatically by the server to ALL tools
   - You don't manually apply this decorator

PARAMETER RULES:

1. NEVER use 'kwargs' as a parameter name
2. ALWAYS use specific, descriptive parameter names
3. ALWAYS include ctx: Context = None as the last parameter
4. ALWAYS use type hints for all parameters
5. ALWAYS provide defaults for optional parameters

COMMON MISTAKES TO AVOID:

1. ❌ async def my_tool(**kwargs):  # NEVER use kwargs
   ✅ async def my_tool(param1: str, param2: int, ctx: Context = None):

2. ❌ def my_tool(...):  # MUST be async
   ✅ async def my_tool(...):

3. ❌ async def my_tool(message: str):  # Missing ctx parameter
   ✅ async def my_tool(message: str, ctx: Context = None):

4. ❌ async def my_tool(param):  # Missing type hints
   ✅ async def my_tool(param: str, ctx: Context = None) -> str:
"""