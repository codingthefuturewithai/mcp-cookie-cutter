"""
REFERENCE PATTERNS FOR MCP DECORATORS - DO NOT DELETE

This file explains how the decorator system works and how to apply
decorators correctly to MCP tools.

CRITICAL: Understanding these patterns is essential for maintaining
MCP compatibility and proper error handling.
"""

from typing import Dict, List, Any, Optional
from fastmcp import Context
import inspect
import functools


# ============================================================================
# DECORATOR APPLICATION ORDER (CRITICAL!)
# ============================================================================

"""
DECORATOR ORDER MATTERS!

The order you apply decorators determines how they wrap each other.
Decorators are applied from bottom to top (inner to outer).

REGULAR TOOLS:
    @exception_handler  # Outer: Catches and re-raises exceptions
    @tool_logger       # Middle: Logs execution details  
    @type_converter    # Inner: Converts MCP string parameters
    async def my_tool(...):
        pass

    Execution flow: 
    1. exception_handler receives call
    2. Calls tool_logger
    3. tool_logger logs start
    4. Calls type_converter
    5. type_converter converts parameters
    6. Calls actual tool
    7. Returns result through chain

PARALLEL TOOLS:
    @exception_handler  # Outermost: Catches exceptions
    @tool_logger       # Middle: Logs execution
    @parallelize       # Transforms signature and parallelizes
    @type_converter    # Inner: Converts parameters for each parallel call
    async def my_tool(...):
        pass

    Execution flow:
    1. exception_handler receives call with kwargs_list
    2. Calls tool_logger
    3. tool_logger logs start
    4. Calls parallelize wrapper
    5. parallelize executes tool in parallel for each item
    6. type_converter runs for each parallel execution
    7. Returns list of results through chain
"""


# ============================================================================
# PATTERN 1: Exception Handler Decorator
# ============================================================================

def exception_handler_pattern(func):
    """
    PATTERN: Exception handler that RE-RAISES exceptions for MCP.
    
    Current implementation:
    - Catches exceptions
    - Logs them (optional)
    - RE-RAISES them for MCP to handle
    - This means test assertions should expect isError = True
    
    CRITICAL: Must preserve function signature for MCP introspection!
    """
    @functools.wraps(func)  # CRITICAL: Preserves function metadata
    async def wrapper(*args, **kwargs):
        try:
            # Call the original function
            result = await func(*args, **kwargs)
            return result
        except Exception as e:
            # Log the exception (optional)
            import logging
            logging.error(f"Exception in {func.__name__}: {str(e)}")
            
            # RE-RAISE for MCP to handle
            # This is why tests check: assert result.isError is True
            raise
    
    # CRITICAL: Copy the original signature
    wrapper.__signature__ = inspect.signature(func)
    return wrapper


# ============================================================================
# PATTERN 2: Tool Logger Decorator
# ============================================================================

def tool_logger_pattern(func, config=None):
    """
    PATTERN: Logger that records execution to unified logging system.
    
    Features:
    - Logs before and after execution
    - Records duration, inputs, outputs
    - Uses correlation IDs for request tracking
    - Preserves function signature
    """
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        import time
        import json
        import logging
        
        logger = logging.getLogger(__name__)
        start_time = time.time()
        tool_name = func.__name__
        
        # Log the input arguments (be careful with sensitive data)
        input_args = {
            "args": args,
            "kwargs": kwargs
        }
        
        logger.info(f"Starting tool execution: {tool_name}")
        
        try:
            # Execute the tool
            result = await func(*args, **kwargs)
            
            # Calculate duration
            duration_ms = (time.time() - start_time) * 1000
            
            # Log successful execution
            logger.info(f"Tool {tool_name} completed successfully in {duration_ms:.2f}ms")
            
            return result
            
        except Exception as e:
            # Log the error
            duration_ms = (time.time() - start_time) * 1000
            logger.error(f"Tool {tool_name} failed after {duration_ms:.2f}ms: {str(e)}")
            
            # RE-RAISE the exception (don't swallow it!)
            raise
    
    # Preserve original signature
    wrapper.__signature__ = inspect.signature(func)
    return wrapper


# ============================================================================
# PATTERN 3: Type Converter Decorator
# ============================================================================

def type_converter_pattern(func):
    """
    PATTERN: Converts string parameters from MCP to correct Python types.
    
    MCP sends ALL parameters as strings. This decorator:
    - Inspects function signature
    - Converts string parameters to expected types
    - Handles: int, float, bool, List, Dict, Optional
    - Preserves function signature
    """
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        # Get function signature
        sig = inspect.signature(func)
        
        # Convert each parameter
        converted_kwargs = {}
        for param_name, param in sig.parameters.items():
            if param_name in kwargs:
                value = kwargs[param_name]
                expected_type = param.annotation
                
                # Skip if no type hint or already correct type
                if expected_type == inspect.Parameter.empty:
                    converted_kwargs[param_name] = value
                    continue
                
                # Convert based on type hint
                try:
                    if expected_type == int:
                        converted_kwargs[param_name] = int(value)
                    elif expected_type == float:
                        converted_kwargs[param_name] = float(value)
                    elif expected_type == bool:
                        # Handle string booleans
                        if isinstance(value, str):
                            converted_kwargs[param_name] = value.lower() in ('true', '1', 'yes')
                        else:
                            converted_kwargs[param_name] = bool(value)
                    elif expected_type == List or str(expected_type).startswith('List'):
                        # Parse JSON string to list
                        import json
                        if isinstance(value, str):
                            converted_kwargs[param_name] = json.loads(value)
                        else:
                            converted_kwargs[param_name] = value
                    elif expected_type == Dict or str(expected_type).startswith('Dict'):
                        # Parse JSON string to dict
                        import json
                        if isinstance(value, str):
                            converted_kwargs[param_name] = json.loads(value)
                        else:
                            converted_kwargs[param_name] = value
                    else:
                        # Keep original value for unknown types
                        converted_kwargs[param_name] = value
                except (ValueError, TypeError, json.JSONDecodeError):
                    # If conversion fails, keep original value
                    converted_kwargs[param_name] = value
            elif param.default != inspect.Parameter.empty:
                # Use default value if parameter not provided
                converted_kwargs[param_name] = param.default
        
        # Call function with converted parameters
        return await func(**converted_kwargs)
    
    # Preserve original signature (important!)
    wrapper.__signature__ = inspect.signature(func)
    return wrapper


# ============================================================================
# PATTERN 4: Parallelize Decorator (TRANSFORMS SIGNATURE!)
# ============================================================================

def parallelize_pattern(func):
    """
    PATTERN: Decorator that transforms function for parallel execution.
    
    CRITICAL: This decorator CHANGES the function signature!
    
    Original signature:
        async def tool(param1: str, param2: int) -> str
    
    Transformed signature:
        async def tool(kwargs_list: List[Dict[str, Any]], ctx: Context = None) -> List[Any]
    
    The kwargs_list contains:
        [
            {"param1": "value1", "param2": 42},
            {"param1": "value2", "param2": 43},
            ...
        ]
    """
    import asyncio
    from typing import List, Dict, Any
    
    @functools.wraps(func)
    async def wrapper(kwargs_list: List[Dict[str, Any]], ctx: Context = None):
        # Validate input
        if not isinstance(kwargs_list, list):
            raise TypeError("Parallel tools require List[Dict] parameter")
        
        for i, kwargs in enumerate(kwargs_list):
            if not isinstance(kwargs, dict):
                raise TypeError(f"Item {i} in kwargs_list must be a dict")
        
        # Handle empty list
        if not kwargs_list:
            return []
        
        # Create tasks for parallel execution
        tasks = []
        for kwargs in kwargs_list:
            # Each task calls the original function with unpacked kwargs
            task = asyncio.create_task(func(**kwargs))
            tasks.append(task)
        
        # Execute all tasks in parallel (fail-fast behavior)
        results = await asyncio.gather(*tasks)
        
        return results
    
    # Create NEW signature for the wrapped function
    import inspect
    from typing import List, Dict, Any
    
    # Build new parameter list
    new_params = [
        inspect.Parameter(
            'kwargs_list',
            inspect.Parameter.POSITIONAL_OR_KEYWORD,
            annotation=List[Dict[str, Any]]
        ),
        inspect.Parameter(
            'ctx',
            inspect.Parameter.POSITIONAL_OR_KEYWORD,
            default=None,
            annotation='Context'
        )
    ]
    
    # Create new signature
    original_sig = inspect.signature(func)
    new_sig = inspect.Signature(
        parameters=new_params,
        return_annotation=List[Any]
    )
    
    wrapper.__signature__ = new_sig
    
    # Update docstring to explain the transformation
    original_params = str(inspect.signature(func))
    wrapper.__doc__ = f"""
Parallelized version of `{func.__name__}`.

Original function signature: {func.__name__}{original_params}

This parallelized version accepts:
    kwargs_list (List[Dict[str, Any]]): List of keyword argument dictionaries
    ctx (Context, optional): MCP context

Each dictionary in kwargs_list should contain the parameters for one execution
of the original function.

Returns:
    List[Any]: Results from parallel execution of all items

{func.__doc__ or ''}
"""
    
    return wrapper


# ============================================================================
# EXAMPLE: How Server Applies Decorators
# ============================================================================

async def server_decorator_application_example():
    """
    EXAMPLE: How the server applies decorators to your tools.
    
    This is what happens in server/app.py:
    """
    from mcp_server_project.decorators import exception_handler, tool_logger, type_converter, parallelize
    from mcp_server_project.tools import example_tools, parallel_example_tools
    from fastmcp import FastMCP
    
    # Create MCP server
    server = FastMCP("Your Server")
    config = {}  # Your config dict
    
    # Regular tools: Apply decorators in correct order
    for tool_func in example_tools:
        # Apply decorators (innermost to outermost)
        decorated = exception_handler(tool_logger(type_converter(tool_func), config))
        
        # Register with server
        server.tool(name=tool_func.__name__)(decorated)
    
    # Parallel tools: Apply decorators including parallelize
    for tool_func in parallel_example_tools:
        # Apply decorators (innermost to outermost)
        decorated = exception_handler(tool_logger(parallelize(type_converter(tool_func)), config))
        
        # Register with server
        server.tool(name=tool_func.__name__)(decorated)
    
    return server


# ============================================================================
# CRITICAL POINTS TO REMEMBER
# ============================================================================

"""
KEY DECORATOR PRINCIPLES:

1. SIGNATURE PRESERVATION:
   - Regular decorators MUST preserve the original signature
   - Only @parallelize is allowed to transform the signature
   - Use @functools.wraps and copy __signature__

2. EXCEPTION HANDLING:
   - Decorators should RE-RAISE exceptions, not swallow them
   - MCP needs to see exceptions to set isError = True
   - Log errors but always re-raise

3. DECORATOR ORDER:
   - Apply from inner to outer (bottom to top in code)
   - exception_handler should be outermost
   - type_converter should be innermost (closest to function)
   - parallelize (if used) wraps type_converter

4. NO KWARGS:
   - NEVER introduce a generic **kwargs parameter
   - Always preserve specific parameter names
   - MCP needs to introspect parameter names

5. TYPE CONVERSION:
   - MCP sends all parameters as strings
   - type_converter handles conversion automatically
   - Based on function's type hints

COMMON DECORATOR MISTAKES:

1. ❌ Breaking signature:
   def bad_decorator(func):
       def wrapper(**kwargs):  # Lost parameter names!
           return func(**kwargs)
       return wrapper
   
   ✅ Preserve signature:
   def good_decorator(func):
       @functools.wraps(func)
       def wrapper(*args, **kwargs):
           result = func(*args, **kwargs)
           return result
       wrapper.__signature__ = inspect.signature(func)
       return wrapper

2. ❌ Swallowing exceptions:
   try:
       result = await func(*args, **kwargs)
   except Exception as e:
       return {"error": str(e)}  # Don't do this!
   
   ✅ Re-raise exceptions:
   try:
       result = await func(*args, **kwargs)
   except Exception as e:
       log_error(e)
       raise  # Let MCP handle it

3. ❌ Wrong decorator order:
   @tool_logger      # Wrong order!
   @exception_handler
   async def tool():
   
   ✅ Correct order:
   @exception_handler  # Outer
   @tool_logger       # Inner
   async def tool():

4. ❌ Forgetting async:
   def wrapper(*args, **kwargs):  # Not async!
       return func(*args, **kwargs)
   
   ✅ Async wrapper:
   async def wrapper(*args, **kwargs):
       return await func(*args, **kwargs)
"""