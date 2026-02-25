"""MCP echo client implementation using FastMCP Client"""

import asyncio
import click
from fastmcp import Client
from fastmcp.client.transports import StdioTransport


@click.command()
@click.argument("message", type=str)
def main(message: str):
    """Send a message to the echo server and print the response."""
    
    async def run_client():
        # Create STDIO transport explicitly with the server command
        transport = StdioTransport(
            command="{{ cookiecutter.__project_slug }}-server",
            args=[],
            env=None
        )
        client = Client(transport)
        
        async with client:
            # Call the echo tool from example_tools
            result = await client.call_tool("echo", {"message": message})
            # Result is accessed via .data property
            return result.data
    
    response = asyncio.run(run_client())
    print(response)


if __name__ == "__main__":
    main()
