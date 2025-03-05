"""MCP SSE server implementation"""

import asyncio
from .server import server

async def _main_async():
    """Run the server in SSE mode."""
    await server.run_sse_async()

def main():
    """Entry point for the SSE server."""
    return asyncio.run(_main_async()) 