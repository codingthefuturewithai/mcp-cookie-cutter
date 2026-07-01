"""MCP test client implementation

A minimal stdio client for exercising the generated server during
development. Demonstrates:
- Calling a tool and reading text content
- Reading structured output (structuredContent) from typed tools
"""

import asyncio
import click
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


def _text_of(result) -> str:
    """Extract the first text block from a CallToolResult."""
    for block in result.content:
        if getattr(block, "type", None) == "text":
            return block.text
    return str(result.content)


async def run_demo(message: str) -> None:
    """Send a message to the echo server and print the responses.

    Args:
        message: The message to echo
    """
    # Create server parameters for stdio connection
    server_params = StdioServerParameters(
        command="{{ cookiecutter.__project_slug }}-server",  # Use the installed script
        args=[],  # No additional args needed
        env=None  # Optional environment variables
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize the connection
            await session.initialize()

            # Call the echo tool from example_tools
            result = await session.call_tool("echo", arguments={"message": message})
            print(_text_of(result))

            # Call a structured-output tool: typed tools also return
            # validated structuredContent alongside the text blocks
            weather = await session.call_tool("get_weather", arguments={"city": "Springfield"})
            print("\nget_weather structured output:")
            print(weather.structuredContent)


@click.command()
@click.argument("message", type=str)
def main(message: str):
    """Send a message to the echo server and print the response."""
    asyncio.run(run_demo(message))


if __name__ == "__main__":
    main()
