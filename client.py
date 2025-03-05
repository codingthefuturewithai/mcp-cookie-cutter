import asyncio
import click
from typing import Optional
from mcp import ClientSession, StdioServerParameters
from mcp.types import TextContent, ImageContent, EmbeddedResource
from mcp.client.stdio import stdio_client


async def fetch_website_content(url: str, user_agent: Optional[str] = None) -> str:
    """
    Fetch website content using the MCP server.
    
    Args:
        url: The URL to fetch content from
        user_agent: Optional user agent string to use for the request
        
    Returns:
        The text content of the website
    """
    # Create server parameters for stdio connection
    server_params = StdioServerParameters(
        command="mcp-web-page-fetcher",  # Use the installed script
        args=[],  # No additional args needed
        env=None  # Optional environment variables
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize the connection
            await session.initialize()
            
            # Prepare arguments
            arguments = {"url": url}
            if user_agent:
                arguments["user_agent"] = user_agent
                
            # Call the fetch tool
            result = await session.call_tool("fetch", arguments=arguments)
            if isinstance(result, TextContent):
                return result.text
            else:
                return str(result)


@click.command()
@click.argument("url", type=str)
@click.option("--user-agent", "-u", help="Custom user agent string")
def main(url: str, user_agent: Optional[str] = None):
    """Fetch website content using the MCP server."""
    content = asyncio.run(fetch_website_content(url, user_agent))
    print(content)


if __name__ == "__main__":
    main()
