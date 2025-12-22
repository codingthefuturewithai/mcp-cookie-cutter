#!/usr/bin/env python3
"""Integration test for client-provided correlation IDs.

This script tests that MCP clients can provide correlation IDs that are
properly used by the tool_logger decorator and stored in the SQLite logs.

USAGE:
    python test_correlation_id_integration.py
    
This is a STANDALONE script that:
1. Starts the MCP server as a subprocess (you don't need it running)
2. Connects as a client and sends correlation IDs with each tool call
3. Verifies the correlation IDs are stored in the SQLite database
4. Shows manual verification steps for the Streamlit UI

REQUIREMENTS:
- Run from the project root directory
- Ensure all dependencies are installed (pip install -e .)
"""

# Set up warning filters BEFORE any imports that might trigger them
import warnings
# Suppress the specific RuntimeWarning about coroutines not being awaited
# This is expected behavior in our logging system where we use synchronous fallback
warnings.filterwarnings("ignore", 
                       message="coroutine 'SQLiteDestination.write' was never awaited",
                       category=RuntimeWarning)
# Also suppress the frozen runpy warning which is normal for subprocess execution
warnings.filterwarnings("ignore", 
                       message=".*found in sys.modules after import.*", 
                       category=RuntimeWarning)

import asyncio
import sqlite3
import uuid
from datetime import timedelta
from pathlib import Path
from typing import Dict, List, Optional
from mcp import ClientSession, types
from mcp.client.stdio import stdio_client, StdioServerParameters
import click
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
# No need to import config - we'll determine paths independently

console = Console()


class CorrelationIDTestClient:
    """MCP client that provides correlation IDs for all tool calls."""
    
    def __init__(self, session: ClientSession):
        self.session = session
        self.trace_id = str(uuid.uuid4())
        self.test_results: Dict[str, Dict] = {}
    
    async def call_tool_with_correlation(
        self, 
        tool_name: str, 
        arguments: dict,
        correlation_id: str,
        progress_callback = None
    ) -> dict:
        """Call an MCP tool with a specific correlation ID."""
        # Create metadata with correlation ID
        meta = {
            "correlationId": correlation_id,
            "traceId": self.trace_id,
            "clientType": "correlation_test_client",
            "testRun": "integration_test"
        }
        
        # Build request with custom metadata
        request = types.ClientRequest(
            types.CallToolRequest(
                method="tools/call",
                params=types.CallToolRequestParams(
                    name=tool_name,
                    arguments=arguments,
                    _meta=meta
                )
            )
        )
        
        console.print(f"[blue]→[/blue] Calling '{tool_name}' with correlation ID: [yellow]{correlation_id}[/yellow]")
        
        try:
            result = await self.session.send_request(
                request, 
                types.CallToolResult,
                progress_callback=progress_callback,
                request_read_timeout_seconds=timedelta(seconds=30)
            )
            
            # Store result for verification
            self.test_results[tool_name] = {
                "correlation_id": correlation_id,
                "success": True,
                "result": result.content if hasattr(result, 'content') else str(result)
            }
            
            console.print(f"[green]✓[/green] {tool_name} completed successfully")
            return result
            
        except Exception as e:
            self.test_results[tool_name] = {
                "correlation_id": correlation_id,
                "success": False,
                "error": str(e)
            }
            console.print(f"[red]✗[/red] {tool_name} failed: {e}")
            raise


def get_sqlite_logs(correlation_id: str) -> List[Dict]:
    """Query SQLite database for logs with a specific correlation ID."""
    # Get the SQLite database path using platformdirs
    import platformdirs
    app_data = platformdirs.user_data_dir("my_mcp_server")
    db_path = Path(app_data) / "unified_logs.db"
    
    if not db_path.exists():
        console.print(f"[red]Database not found at {db_path}[/red]")
        return []
    
    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # Query logs for the correlation ID
        cursor.execute("""
            SELECT timestamp, tool_name, duration_ms, status, 
                   input_args, output_summary, error_message
            FROM unified_logs
            WHERE correlation_id = ?
            ORDER BY timestamp
        """, (correlation_id,))
        
        results = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return results
        
    except Exception as e:
        console.print(f"[red]Error querying database: {e}[/red]")
        return []


async def test_all_tools(server_script_path: str):
    """Test all example tools with correlation IDs."""
    
    # Server params for stdio transport with warning suppression
    import os
    env = os.environ.copy()
    # Set Python to not show warnings in the subprocess
    env['PYTHONWARNINGS'] = 'ignore::RuntimeWarning'
    
    server_params = StdioServerParameters(
        command="python",
        args=["-m", "my_mcp_server.server.app", "--transport", "stdio"],
        env=env
    )
    
    console.print(Panel.fit("🧪 [bold]Correlation ID Integration Test[/bold]", border_style="blue"))
    console.print(f"Starting MCP server from: {server_script_path}")
    console.print()
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            client = CorrelationIDTestClient(session)
            
            # Initialize the session
            await session.initialize()
            
            # List available tools
            tools = await session.list_tools()
            console.print(f"[dim]Found {len(tools.tools)} tools[/dim]")
            console.print()
            
            # Define test cases for all tools
            test_cases = [
                {
                    "tool": "echo",
                    "args": {"message": "Testing correlation ID feature!"},
                    "correlation_id": "test_echo_abc123"
                },
                {
                    "tool": "get_time",
                    "args": {},
                    "correlation_id": "test_time_def456"
                },
                {
                    "tool": "random_number",
                    "args": {"min_value": 1, "max_value": 100},
                    "correlation_id": "test_random_ghi789"
                },
                {
                    "tool": "calculate_fibonacci",
                    "args": {"n": 10},
                    "correlation_id": "test_fib_jkl012"
                },
                {
                    "tool": "simulate_heavy_computation",
                    "args": {"kwargs_list": [{"complexity": 3}, {"complexity": 4}]},
                    "correlation_id": "test_compute_mno345"
                },
                {
                    "tool": "process_batch_data",
                    "args": {"kwargs_list": [{"items": ["item1", "item2"], "operation": "upper"}, {"items": ["item3"], "operation": "lower"}]},
                    "correlation_id": "test_batch_pqr678"
                }
            ]
            
            # Test each tool
            console.print("[bold]Testing all example tools:[/bold]")
            for test_case in test_cases:
                # Progress callback for heavy computation
                def on_progress(progress, total, message):
                    if test_case["tool"] == "simulate_heavy_computation":
                        console.print(f"  [dim]Progress: {progress}/{total} - {message}[/dim]")
                
                try:
                    await client.call_tool_with_correlation(
                        test_case["tool"],
                        test_case["args"],
                        test_case["correlation_id"],
                        progress_callback=on_progress if "heavy" in test_case["tool"] else None
                    )
                except Exception:
                    pass  # Error already logged
                
                await asyncio.sleep(0.1)  # Small delay between calls
            
            console.print()
            
            # Verify results in SQLite
            console.print("[bold]Verifying correlation IDs in SQLite logs:[/bold]")
            console.print()
            
            verification_table = Table(title="SQLite Log Verification")
            verification_table.add_column("Tool", style="cyan")
            verification_table.add_column("Expected ID", style="yellow")
            verification_table.add_column("Found in DB", style="green")
            verification_table.add_column("Status", style="bold")
            
            all_verified = True
            
            for test_case in test_cases:
                tool_name = test_case["tool"]
                expected_id = test_case["correlation_id"]
                
                # Query SQLite for this correlation ID
                logs = get_sqlite_logs(expected_id)
                
                if logs:
                    found = "✓ Yes"
                    status = "[green]PASSED[/green]"
                    
                    # Show log details
                    console.print(f"\n[dim]Logs for {tool_name} ({expected_id}):[/dim]")
                    for log in logs:
                        console.print(f"  • {log['timestamp']}: {log['tool_name']} - "
                                    f"Status: {log['status']}, Duration: {log['duration_ms']}ms")
                else:
                    found = "✗ No"
                    status = "[red]FAILED[/red]"
                    all_verified = False
                
                verification_table.add_row(tool_name, expected_id, found, status)
            
            console.print()
            console.print(verification_table)
            console.print()
            
            # Summary for WITH correlation IDs
            if all_verified:
                console.print("[bold green]✅ SUCCESS:[/bold green] All client-provided correlation IDs were properly logged!")
            else:
                console.print("[bold red]❌ FAILURE:[/bold red] Some client-provided correlation IDs were not found in logs")
                console.print("\n[yellow]Troubleshooting:[/yellow]")
                console.print("1. Ensure the server is using the updated tool_logger decorator")
                console.print("2. Check that SQLite logging destination is enabled in config.yaml")
                console.print("3. Verify the database path is correct for your platform")
            
            console.print("\n" + "="*80 + "\n")
            
            # Test WITHOUT client-provided correlation IDs
            console.print("[bold]Testing all example tools WITHOUT client-provided correlation IDs:[/bold]")
            console.print("[dim]These should auto-generate correlation IDs in the format 'req_01ARZ3NDEKTSV4RRFFQ69G5FAV' (ULID)[/dim]")
            console.print()
            
            # Define test cases without correlation IDs
            test_cases_no_id = [
                {"tool": "echo", "args": {"message": "Testing auto-generated ID!"}},
                {"tool": "get_time", "args": {}},
                {"tool": "random_number", "args": {"min_value": 10, "max_value": 50}},
                {"tool": "calculate_fibonacci", "args": {"n": 15}},
                {"tool": "simulate_heavy_computation", "args": {"kwargs_list": [{"complexity": 2}]}},
                {"tool": "process_batch_data", "args": {"kwargs_list": [{"items": ["test1", "test2"], "operation": "reverse"}]}}
            ]
            
            auto_generated_ids = {}
            
            for test_case in test_cases_no_id:
                tool_name = test_case["tool"]
                
                # Call tool WITHOUT correlation ID
                console.print(f"[blue]→[/blue] Calling '{tool_name}' WITHOUT correlation ID")
                
                try:
                    # Standard MCP call without custom metadata
                    request = types.ClientRequest(
                        types.CallToolRequest(
                            method="tools/call",
                            params=types.CallToolRequestParams(
                                name=tool_name,
                                arguments=test_case["args"]
                            )
                        )
                    )
                    
                    result = await session.send_request(
                        request,
                        types.CallToolResult,
                        request_read_timeout_seconds=timedelta(seconds=30)
                    )
                    
                    console.print(f"[green]✓[/green] {tool_name} completed successfully")
                    
                    # Sleep briefly to ensure logs are written
                    await asyncio.sleep(0.2)
                    
                    # Query for the most recent log entry for this tool
                    import platformdirs
                    app_data = platformdirs.user_data_dir("my_mcp_server")
                    db_path = Path(app_data) / "unified_logs.db"
                    
                    if db_path.exists():
                        conn = sqlite3.connect(db_path)
                        conn.row_factory = sqlite3.Row
                        cursor = conn.cursor()
                        
                        # Get the most recent tool execution log for this tool
                        cursor.execute("""
                            SELECT correlation_id 
                            FROM unified_logs 
                            WHERE tool_name = ? AND status = 'success'
                            ORDER BY timestamp DESC 
                            LIMIT 1
                        """, (tool_name,))
                        
                        row = cursor.fetchone()
                        if row:
                            auto_generated_ids[tool_name] = row['correlation_id']
                            console.print(f"  [yellow]Auto-generated ID: {row['correlation_id']}[/yellow]")
                        else:
                            console.print(f"  [red]No correlation ID found in logs[/red]")
                        
                        conn.close()
                    
                except Exception as e:
                    console.print(f"[red]✗[/red] {tool_name} failed: {e}")
                
                await asyncio.sleep(0.1)
            
            console.print()
            
            # Verify auto-generated IDs
            console.print("[bold]Verifying auto-generated correlation IDs:[/bold]")
            console.print()
            
            auto_gen_table = Table(title="Auto-Generated Correlation ID Verification")
            auto_gen_table.add_column("Tool", style="cyan")
            auto_gen_table.add_column("Generated ID", style="yellow")
            auto_gen_table.add_column("Format Valid", style="green")
            auto_gen_table.add_column("Status", style="bold")
            
            all_auto_verified = True
            
            for tool_name, correlation_id in auto_generated_ids.items():
                if correlation_id and correlation_id.startswith("req_") and len(correlation_id) > 4:
                    format_valid = "✓ Yes"
                    status = "[green]PASSED[/green]"
                else:
                    format_valid = "✗ No"
                    status = "[red]FAILED[/red]"
                    all_auto_verified = False
                
                auto_gen_table.add_row(
                    tool_name,
                    correlation_id if correlation_id else "None",
                    format_valid,
                    status
                )
            
            console.print(auto_gen_table)
            console.print()
            
            if all_auto_verified:
                console.print("[bold green]✅ SUCCESS:[/bold green] All tools auto-generated correlation IDs correctly!")
            else:
                console.print("[bold red]❌ FAILURE:[/bold red] Some tools did not auto-generate correlation IDs correctly")
            
            # Manual verification instructions
            console.print("\n[bold]Manual Verification Instructions:[/bold]")
            console.print("1. Run the Streamlit UI: [cyan]streamlit run my_mcp_server/ui/app.py[/cyan]")
            console.print("2. Navigate to the Logs page")
            console.print("3. Use the Correlation ID filter to search for:")
            for test_case in test_cases:
                console.print(f"   • {test_case['correlation_id']}")
            console.print("4. Verify that each correlation ID shows the corresponding tool execution")
            
            # Show database location
            db_path = Path.home() / ".local" / "share" / "my_mcp_server" / "unified_logs.db"
            console.print(f"\n[dim]SQLite database location: {db_path}[/dim]")


@click.command()
@click.option(
    '--server-module',
    default="my_mcp_server.server.app",
    help='Python module path to the MCP server'
)
def main(server_module: str):
    """Test correlation ID integration with all example tools.
    
    This script:
    1. Starts the MCP server
    2. Calls all example tools with unique correlation IDs
    3. Verifies the correlation IDs were stored in SQLite logs
    4. Provides instructions for manual verification
    """
    asyncio.run(test_all_tools(server_module))


if __name__ == "__main__":
    main()