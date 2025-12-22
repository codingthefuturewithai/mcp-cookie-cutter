"""MCP echo client implementation"""

import asyncio
import click
from mcp import ClientSession, StdioServerParameters
from mcp.types import TextContent
from mcp.client.stdio import stdio_client


async def echo_message(message: str) -> str:
    """
    Send a message to the echo server and get the response.
    
    Args:
        message: The message to echo
        
    Returns:
        The echoed message from the server
    """
    # Create server parameters for stdio connection
    server_params = StdioServerParameters(
        command="my_mcp_server-server",  # Use the installed script
        args=[],  # No additional args needed
        env=None  # Optional environment variables
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize the connection
            await session.initialize()
            
            # Call the echo tool from example_tools
            arguments = {"message": message}
                
            result = await session.call_tool("echo", arguments=arguments)
            if isinstance(result, TextContent):
                return result.text
            else:
                return str(result)


@click.command()
@click.argument("message", type=str)
def main(message: str):
    """Send a message to the echo server and print the response."""
    response = asyncio.run(echo_message(message))
    print(response)


if __name__ == "__main__":
    main() 