"""Example MCP tools for {{ cookiecutter.project_name }}

This module provides example tools that demonstrate how to create MCP tools
with the decorator pattern. These tools are automatically registered
with the server and decorated with exception handling, logging, and optional
parallelization.
"""

import time
import random
from typing import List, Dict, Any
from fastmcp import Context
from pydantic import BaseModel, Field
import mcp.types
from {{cookiecutter.__project_slug}}.log_system.unified_logger import UnifiedLogger

async def echo(message: str, ctx: Context = None) -> str:
    """Echo back the input message.
    
    This is a simple example tool that demonstrates basic MCP tool functionality.
    It will be automatically decorated with decorators for exception handling
    and logging.
    
    Args:
        message: The message to echo back
        
    Returns:
        The echoed message with a prefix
    """
    return f"Echo: {message}"


async def get_time(ctx: Context = None) -> str:
    """Get the current time.
    
    Returns the current time in a human-readable format.
    
    Returns:
        Current time as a string
    """
    logger = UnifiedLogger.get_logger(__name__)
    logger.info("get_time called to retrieve current time")
    return f"Current time: {time.strftime('%Y-%m-%d %H:%M:%S')}"


async def random_number(min_value: int = 1, max_value: int = 100, ctx: Context = None) -> Dict[str, Any]:
    """Generate a random number within a specified range.
    
    Args:
        min_value: Minimum value (default: 1)
        max_value: Maximum value (default: 100)
        
    Returns:
        Dictionary containing the random number and range info
    """
    logger = UnifiedLogger.get_logger(__name__)
    logger.info(f"random_number called with range {min_value}-{max_value}")
    if min_value > max_value:
        raise ValueError("min_value must be less than or equal to max_value")
    
    number = random.randint(min_value, max_value)
    return {
        "number": number,
        "range": f"{min_value}-{max_value}",
        "timestamp": time.time()
    }


async def calculate_fibonacci(n: int, ctx: Context = None) -> Dict[str, Any]:
    """Calculate the nth Fibonacci number.
    
    This is a more computationally intensive example that demonstrates
    how tools can handle more complex operations.
    
    Args:
        n: The position in the Fibonacci sequence (must be >= 0)
        
    Returns:
        Dictionary containing the Fibonacci number and calculation info
    """
    logger = UnifiedLogger.get_logger(__name__)
    logger.info(f"calculate_fibonacci called for position {n}")
    if n < 0:
        raise ValueError("n must be non-negative")
    
    if n <= 1:
        return {"position": n, "value": n, "calculation_time": 0}
    
    start_time = time.time()
    
    # Calculate Fibonacci number
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    
    calculation_time = time.time() - start_time
    
    return {
        "position": n,
        "value": b,
        "calculation_time": calculation_time
    }


async def search_tool(
    query: str,
    max_results: int = 10,
    directories: list[str] = [],
    include_hidden: bool = False,
    ctx: Context = None
) -> Dict[str, Any]:
    """Search for content with optional filters.
    
    This tool demonstrates optional parameters that commonly cause issues
    with certain MCP clients. It tests type conversion for optional types.
    
    Args:
        query: Search query string (required)
        max_results: Maximum number of results to return (optional)
        directories: List of directories to search in (optional)
        include_hidden: Whether to include hidden files (optional)
        ctx: MCP Context object (optional, provided by MCP runtime)
        
    Returns:
        Search results with applied filters
    """
    logger = UnifiedLogger.get_logger(__name__)
    logger.info(f"search_tool called with query: {query}")
    # Handle empty directories list -> use default directory
    actual_dirs = directories if directories else ["default_dir"]
    
    # Simulate search results
    results = []
    for i in range(min(max_results, 5)):  # Cap at 5 for demo
        results.append({
            "id": i + 1,
            "title": f"Result {i + 1} for '{query}'",
            "directory": actual_dirs[i % len(actual_dirs)],
            "hidden": include_hidden
        })
    
    return {
        "query": query,
        "max_results": max_results,
        "directories": actual_dirs,
        "include_hidden": include_hidden,
        "result_count": len(results),
        "results": results,
        "message": f"Found {len(results)} results for '{query}' in {len(actual_dirs)} directories"
    }

class BookingPreferences(BaseModel):
    """Schema for collecting user preferences."""

    checkAlternative: bool = Field(description="Would you like to check another date?")
    alternativeDate: str = Field(
        default="2024-12-26",
        description="Alternative date (YYYY-MM-DD)",
    )

async def elicit_example(date: str, time: str, party_size: int, ctx: Context = None) -> str:
    """Book a table with date availability check."""
    logger = UnifiedLogger.get_logger(__name__)
    logger.info(f"elicit_example called for date: {date}, party_size: {party_size}")
    # Check if date is available
    if date == "2024-12-25":
        # Date unavailable - ask user for alternative
        result = await ctx.elicit(
            message=(f"No tables available for {party_size} on {date}. Would you like to try another date?"),
            response_type=BookingPreferences,
        )

        if result.action == "accept" and result.data:
            if result.data.checkAlternative:
                return f"[SUCCESS] Booked for {result.data.alternativeDate}"
            return "[CANCELLED] No booking made"
        return "[CANCELLED] Booking cancelled"

    # Date available
    return f"[SUCCESS] Booked for {date} at {time}"

async def notification_example(data: str, ctx: Context = None) -> str:
    """Process data with logging."""
    logger = UnifiedLogger.get_logger(__name__)
    logger.info(f"notification_example called with data: {data}")
    # Different log levels
    await ctx.debug(f"Debug: Processing '{data}'")
    await ctx.info("Info: Starting processing")
    await ctx.warning("Warning: This is experimental")
    await ctx.error("Error: (This is just a demo)")

    # Notify about resource changes
    await ctx.send_notification(mcp.types.ResourceListChangedNotification())

    return f"Processed: {data}"

async def progress_example(task_name: str, ctx: Context = None, steps: int = 5) -> str:
    """Execute a task with progress updates."""
    logger = UnifiedLogger.get_logger(__name__)
    logger.info(f"progress_example called for task: {task_name}")
    await ctx.info(f"Starting: {task_name}")

    for i in range(steps):
        progress = (i + 1) / steps
        await ctx.report_progress(
            progress=progress,
            total=1.0,
        )
        await ctx.debug(f"Completed step {i + 1}")

    return f"Task '{task_name}' completed"


async def process_batch_data(items: List[str], operation: str = "upper", ctx: Context = None) -> Dict[str, Any]:
    """Process a batch of data items.
    
    This is an example of a tool that benefits from parallelization.
    It will be automatically decorated with the parallelize decorator
    in addition to exception handling and logging.
    
    Args:
        items: List of strings to process
        operation: Operation to perform ('upper', 'lower', 'reverse')
        
    Returns:
        Processed items with metadata
    """
    logger = UnifiedLogger.get_logger(__name__)
    logger.info(f"process_batch_data called with {len(items)} items, operation: {operation}")
    # Simulate some processing time
    import asyncio
    await asyncio.sleep(0.1)
    
    processed_items = []
    for item in items:
        if operation == "upper":
            processed = item.upper()
        elif operation == "lower":
            processed = item.lower()
        elif operation == "reverse":
            processed = item[::-1]
        else:
            raise ValueError(f"Unknown operation: {operation}")
        processed_items.append(processed)
    
    return {
        "original": items,
        "processed": processed_items,
        "operation": operation,
        "timestamp": time.time()
    }


async def simulate_heavy_computation(complexity: int = 5, ctx: Context = None) -> Dict[str, Any]:
    """Simulate a heavy computation task.
    
    This tool demonstrates parallelization benefits by performing
    a computationally intensive task that can be parallelized.
    
    Args:
        complexity: Complexity level (1-10, higher = more computation)
        
    Returns:
        Dictionary containing computation results
    """
    logger = UnifiedLogger.get_logger(__name__)
    logger.info(f"simulate_heavy_computation called with complexity: {complexity}")
    if complexity < 1 or complexity > 10:
        raise ValueError("complexity must be between 1 and 10")
    
    start_time = time.time()
    
    # Simulate heavy computation
    result = 0
    iterations = complexity * 100000  # Reduced for async context
    
    for i in range(iterations):
        result += i * 2
        if i % 10000 == 0:
            # Yield control to allow other tasks to run
            import asyncio
            await asyncio.sleep(0.001)
    
    computation_time = time.time() - start_time
    
    return {
        "complexity": complexity,
        "iterations": iterations,
        "result": result,
        "computation_time": computation_time,
        "operations_per_second": iterations / computation_time if computation_time > 0 else 0
    }


# List of tools that benefit from parallelization
parallel_example_tools = [
    process_batch_data,
    simulate_heavy_computation
]

# List of regular example tools
example_tools = [
    echo,
    get_time,
    random_number,
    calculate_fibonacci,
    search_tool,
    elicit_example,
    notification_example,
    progress_example
]

async def get_tool_info() -> Dict[str, Any]:
    """Get information about available tools.
    
    Returns:
        Dictionary containing tool information
    """
    return {
        "total_tools": len(example_tools) + len(parallel_example_tools),
        "regular_tools": len(example_tools),
        "parallel_tools": len(parallel_example_tools),
        "tool_names": {
            "regular": [tool.__name__ for tool in example_tools],
            "parallel": [tool.__name__ for tool in parallel_example_tools]
        }
    }


if __name__ == "__main__":
    # Test tools functionality
    import asyncio
    
    async def test_tools():
        print("Tool Information:")
        print(await get_tool_info())
        
        print("\nTesting example tools:")
        print(await echo("Hello, World!"))
        print(await get_time())
        print(await random_number(1, 10))
        print(await calculate_fibonacci(10))
        
        print("\nTesting parallel tools (individual calls):")
        print(await process_batch_data(["hello", "world"], "upper"))
        print(await simulate_heavy_computation(2))
    
    asyncio.run(test_tools())