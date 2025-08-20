"""Type Converter Decorator for MCP Tools - Handles Runtime Type Conversion.

This decorator handles runtime type conversion for MCP tools when clients send
incorrect types (e.g., strings instead of integers). This is particularly important
for certain MCP clients that may send all parameters as strings.

The decorator:
1. Converts string inputs to proper types based on function annotations
2. Handles int, float, bool, List, Dict conversions
3. Preserves function signatures for MCP introspection
4. Handles Optional types gracefully

This is a RUNTIME conversion, not a schema modification. The schema remains
unchanged to maintain MCP compatibility.
"""

import inspect
import json
from functools import wraps
from typing import Any, Callable, Dict, List, Optional, Union, get_args, get_origin
import asyncio


def type_converter(func: Callable) -> Callable:
    """Convert string parameters to their proper types based on function annotations.
    
    This decorator performs runtime type conversion for MCP tools. Many MCP clients
    send all parameters as strings, requiring server-side conversion to the proper types.
    
    Supported conversions:
    - str -> int
    - str -> float  
    - str -> bool (handles "true"/"false", "True"/"False", "1"/"0")
    - str -> List (parses JSON strings)
    - str -> Dict (parses JSON strings)
    - Handles Optional types by checking for None first
    
    Args:
        func: The function to decorate
        
    Returns:
        The decorated function with type conversion applied
    """
    sig = inspect.signature(func)
    
    @wraps(func)
    async def async_wrapper(*args, **kwargs):
        """Async wrapper that performs type conversion."""
        return await _convert_and_call(func, sig, args, kwargs, is_async=True)
    
    @wraps(func)
    def sync_wrapper(*args, **kwargs):
        """Sync wrapper that performs type conversion."""
        return _convert_and_call(func, sig, args, kwargs, is_async=False)
    
    # Return appropriate wrapper based on function type
    if asyncio.iscoroutinefunction(func):
        # Preserve original signature and metadata
        async_wrapper.__signature__ = sig
        async_wrapper.__annotations__ = func.__annotations__
        return async_wrapper
    else:
        sync_wrapper.__signature__ = sig
        sync_wrapper.__annotations__ = func.__annotations__
        return sync_wrapper


def _convert_and_call(func: Callable, sig: inspect.Signature, args: tuple, kwargs: dict, is_async: bool) -> Any:
    """Convert parameters and call the function.
    
    Args:
        func: The original function
        sig: The function signature
        args: Positional arguments
        kwargs: Keyword arguments
        is_async: Whether the function is async
        
    Returns:
        The function result
    """
    # Convert kwargs based on function signature
    converted_kwargs = {}
    
    for param_name, param in sig.parameters.items():
        # Skip if parameter not provided
        if param_name not in kwargs:
            # Use default if available
            if param.default != inspect.Parameter.empty:
                converted_kwargs[param_name] = param.default
            continue
        
        value = kwargs[param_name]
        
        # Skip if already None (for Optional types)
        if value is None:
            converted_kwargs[param_name] = None
            continue
        
        # Get the annotation for type conversion
        annotation = param.annotation
        
        # Skip if no annotation
        if annotation == inspect.Parameter.empty:
            converted_kwargs[param_name] = value
            continue
        
        # Handle Optional types
        origin = get_origin(annotation)
        if origin is Union:
            # For Optional[X], get the non-None type
            args_types = get_args(annotation)
            # Filter out NoneType
            non_none_types = [t for t in args_types if t != type(None)]
            if non_none_types:
                annotation = non_none_types[0]
                origin = get_origin(annotation)
        
        # Perform type conversion
        try:
            converted_value = _convert_value(value, annotation, origin)
            converted_kwargs[param_name] = converted_value
        except (ValueError, TypeError, json.JSONDecodeError) as e:
            # If conversion fails, pass through original value
            # Let the function handle the type error
            converted_kwargs[param_name] = value
    
    # Call the function with converted parameters
    if is_async:
        return func(**converted_kwargs)
    else:
        return func(**converted_kwargs)


def _convert_value(value: Any, target_type: type, origin: Optional[type]) -> Any:
    """Convert a single value to the target type.
    
    Args:
        value: The value to convert
        target_type: The target type annotation
        origin: The origin type for generics (e.g., List, Dict)
        
    Returns:
        The converted value
    """
    # If already the correct type, return as-is
    if isinstance(value, target_type) and origin is None:
        return value
    
    # Handle string conversions
    if isinstance(value, str):
        # Convert to int
        if target_type == int:
            return int(value)
        
        # Convert to float
        elif target_type == float:
            return float(value)
        
        # Convert to bool
        elif target_type == bool:
            return _str_to_bool(value)
        
        # Convert to List
        elif origin is list or target_type == list:
            if value.startswith('[') and value.endswith(']'):
                return json.loads(value)
            else:
                # Single value to list
                return [value]
        
        # Convert to Dict
        elif origin is dict or target_type == dict:
            if value.startswith('{') and value.endswith('}'):
                return json.loads(value)
            else:
                raise ValueError(f"Cannot convert '{value}' to dict")
    
    # Handle list to List[type] conversions
    elif isinstance(value, list) and (origin is list or target_type == list):
        # Get the element type if specified
        if origin is list:
            element_types = get_args(target_type)
            if element_types:
                element_type = element_types[0]
                # Convert each element if needed
                return [_convert_value(item, element_type, get_origin(element_type)) 
                        if not isinstance(item, element_type) else item 
                        for item in value]
        return value
    
    # No conversion needed or possible
    return value


def _str_to_bool(value: str) -> bool:
    """Convert string to boolean.
    
    Args:
        value: String value to convert
        
    Returns:
        Boolean value
        
    Raises:
        ValueError: If string cannot be converted to boolean
    """
    if value.lower() in ('true', '1', 'yes', 'on'):
        return True
    elif value.lower() in ('false', '0', 'no', 'off'):
        return False
    else:
        raise ValueError(f"Cannot convert '{value}' to bool")