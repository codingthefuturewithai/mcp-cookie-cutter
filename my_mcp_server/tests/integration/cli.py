"""CLI commands for MCP integration testing.

Provides developer-friendly commands for:
- Running MCP integration tests with nice output
- Generating test templates for new MCP tools
"""

import asyncio
import sys
from pathlib import Path
from typing import Optional
import pytest
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.syntax import Syntax


console = Console()


def run_integration_tests(tool: Optional[str] = None, verbose: bool = False) -> int:
    """Run MCP integration tests with nice output.
    
    Args:
        tool: Optional specific tool name to test
        verbose: Enable verbose pytest output
        
    Returns:
        Exit code (0 for success, non-zero for failure)
    """
    console.print(Panel.fit(
        "[bold blue]Running MCP Integration Tests[/bold blue]",
        subtitle="Testing tools as real MCP clients would use them"
    ))
    
    # Build pytest arguments
    test_dir = Path(__file__).parent
    pytest_args = [
        str(test_dir / "test_example_tools_integration.py"),
        "-v" if verbose else "-q",
        "--tb=short",
        "--color=yes"
    ]
    
    # Add specific test filter if tool specified
    if tool:
        pytest_args.extend(["-k", tool])
        console.print(f"[yellow]Testing specific tool: {tool}[/yellow]\n")
    
    # Run pytest
    exit_code = pytest.main(pytest_args)
    
    # Print results
    console.print()
    if exit_code == 0:
        console.print("[bold green]✓ All MCP integration tests passed![/bold green]")
    else:
        console.print("[bold red]✗ Some tests failed[/bold red]")
        console.print("[yellow]Run with --verbose for detailed output[/yellow]")
    
    return exit_code


def generate_tool_tests(tool_name: Optional[str] = None) -> int:
    """Generate test templates for new MCP tools.
    
    Args:
        tool_name: Name of the tool to generate tests for
        
    Returns:
        Exit code (0 for success, non-zero for failure)
    """
    if not tool_name:
        # Check command line args
        if len(sys.argv) > 1:
            tool_name = sys.argv[1]
        else:
            console.print("[red]Usage: generate-mcp-tests TOOL_NAME[/red]")
            console.print("Example: generate-mcp-tests my_custom_tool")
            return 1
    
    # Generate test template
    test_template = '''async def test_{}_execution(self, mcp_session: ClientSession):
    """Test {} execution via MCP client."""
    # TODO: Add appropriate parameters for {}
    result = await mcp_session.call_tool("{}", {{
        # "param1": "value1",
        # "param2": "value2"
    }})
    
    assert not result.isError, f"Tool execution failed: {{result}}"
    
    # TODO: Add assertions for expected output
    text_content = self._extract_text_content(result)
    assert text_content is not None, "No text content returned"
    
    # Example: Check for specific content in response
    # assert "expected_text" in text_content
    # 
    # Example: Parse JSON response
    # try:
    #     data = json.loads(text_content)
    #     assert data["field"] == expected_value
    # except json.JSONDecodeError:
    #     pytest.fail(f"Invalid JSON response: {{text_content}}")

async def test_{}_error_handling(self, mcp_session: ClientSession):
    """Test {} error handling."""
    # TODO: Test with invalid parameters
    result = await mcp_session.call_tool("{}", {{
        # Invalid parameters to trigger error
    }})
    
    assert result.isError, "Should return error for invalid parameters"
    
    error_text = self._extract_error_text(result)
    assert error_text, "No error text found"
    # TODO: Check for specific error message
'''.format(tool_name, tool_name, tool_name, tool_name, tool_name, tool_name, tool_name)
    
    # Display generated template
    console.print(Panel.fit(
        f"[bold green]Generated MCP Integration Test for: {tool_name}[/bold green]",
        subtitle="Add this to YOUR test file (e.g., test_your_tool.py)"
    ))
    
    syntax = Syntax(test_template, "python", theme="monokai", line_numbers=True)
    console.print(syntax)
    
    console.print("\n[bold yellow]Next Steps:[/bold yellow]")
    console.print("1. Copy the generated test to YOUR test file (e.g., test_your_tool.py)")
    console.print("2. Update the test parameters based on your tool's requirements")
    console.print("3. Add appropriate assertions for the expected output")
    console.print("4. Run the test with: [cyan]test-mcp-integration --tool " + tool_name + "[/cyan]")
    
    return 0


def list_tools() -> int:
    """List all tools that have integration tests."""
    console.print(Panel.fit(
        "[bold blue]MCP Tools with Integration Tests[/bold blue]"
    ))
    
    # Define tools
    tools = [
        ("echo_tool", "Echo back input message", "Basic"),
        ("get_time", "Get current time", "Basic"),
        ("random_number", "Generate random number", "Basic"),
        ("calculate_fibonacci", "Calculate Fibonacci number", "Basic"),
    ]
    
    tools.extend([
        ("process_batch_data", "Process data in parallel", "Parallel"),
        ("simulate_heavy_computation", "Simulate computation", "Parallel"),
    ])
    
    # Create table
    table = Table(title="Available Tools")
    table.add_column("Tool Name", style="cyan", no_wrap=True)
    table.add_column("Description", style="white")
    table.add_column("Type", style="yellow")
    
    for name, desc, tool_type in tools:
        table.add_row(name, desc, tool_type)
    
    console.print(table)
    console.print("\n[yellow]Run specific tool test with:[/yellow] test-mcp-integration --tool TOOL_NAME")
    
    return 0


def main():
    """Main entry point for CLI commands."""
    import argparse
    
    parser = argparse.ArgumentParser(description="MCP Integration Testing CLI")
    parser.add_argument("--tool", help="Test specific tool")
    parser.add_argument("--verbose", action="store_true", help="Verbose output")
    parser.add_argument("--list", action="store_true", help="List available tools")
    parser.add_argument("--generate", help="Generate test for new tool")
    
    args = parser.parse_args()
    
    if args.list:
        return list_tools()
    elif args.generate:
        return generate_tool_tests(args.generate)
    else:
        return run_integration_tests(tool=args.tool, verbose=args.verbose)


# Entry points for setuptools
def run_tests_entry():
    """Entry point for test-mcp-integration command."""
    sys.exit(main())


# Note: The generate_tests_entry function below is deprecated
# Test generation is now handled by Claude Code's /generate-tests command
# which provides much more comprehensive and intelligent test generation
# We keep this for backwards compatibility but it's not exposed as a script


if __name__ == "__main__":
    sys.exit(main())