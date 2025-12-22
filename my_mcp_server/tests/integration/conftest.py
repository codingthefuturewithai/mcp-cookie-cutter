"""Integration test configuration with multi-transport support.

This module provides pytest fixtures for testing MCP servers across multiple
transport protocols (STDIO and Streamable HTTP).
"""

import asyncio
import os
import sys
import subprocess
import time
import signal
import atexit
import psutil
from pathlib import Path
from typing import AsyncGenerator, Tuple, Optional, List
import pytest
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client, get_default_environment

# Conditional import for streamable_http
try:
    from mcp.client.streamable_http import streamablehttp_client
    HAS_STREAMABLE_HTTP = True
except ImportError:
    HAS_STREAMABLE_HTTP = False
    streamablehttp_client = None


# Mark all tests in this module as async
pytestmark = pytest.mark.anyio


class StreamableHTTPServer:
    """Manager for Streamable HTTP server process with guaranteed cleanup."""
    
    # Class-level tracking of all server instances for cleanup
    _active_servers: List['StreamableHTTPServer'] = []
    
    def __init__(self, port: int = 3001):
        self.port = port
        self.process: Optional[subprocess.Popen] = None
        self.project_root = Path(__file__).parent.parent.parent
        self.server_module = "my_mcp_server.server.app"
        self._cleanup_registered = False
    
    def start(self) -> None:
        """Start the Streamable HTTP server in a subprocess."""
        if self.process is not None:
            return
        
        # Kill any existing process on this port first
        self._kill_port_processes()
        
        # Build environment
        env = os.environ.copy()
        env["PYTHONPATH"] = str(self.project_root)
        
        # Start server process
        self.process = subprocess.Popen(
            [sys.executable, "-m", self.server_module, "--transport", "streamable-http", "--port", str(self.port)],
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=str(self.project_root)
        )
        
        # Register for cleanup
        if not self._cleanup_registered:
            StreamableHTTPServer._active_servers.append(self)
            self._cleanup_registered = True
        
        # Wait for server to be ready
        time.sleep(2)  # Give server time to start
        
        # Check if process is still running
        if self.process.poll() is not None:
            stdout, stderr = self.process.communicate()
            raise RuntimeError(f"Server failed to start. stdout: {stdout.decode()}, stderr: {stderr.decode()}")
    
    def stop(self) -> None:
        """Stop the Streamable HTTP server with multiple fallback strategies."""
        if self.process is None:
            return
        
        try:
            # Try graceful termination first
            self.process.terminate()
            try:
                self.process.wait(timeout=2)
            except subprocess.TimeoutExpired:
                # Force kill if termination didn't work
                self.process.kill()
                try:
                    self.process.wait(timeout=2)
                except subprocess.TimeoutExpired:
                    # Use OS-level kill as last resort
                    if self.process.pid:
                        try:
                            # Windows doesn't have SIGKILL, use platform-appropriate method
                            if sys.platform == "win32":
                                # On Windows, forcefully terminate the process
                                import ctypes
                                kernel32 = ctypes.windll.kernel32
                                handle = kernel32.OpenProcess(1, False, self.process.pid)
                                kernel32.TerminateProcess(handle, 1)
                                kernel32.CloseHandle(handle)
                            else:
                                os.kill(self.process.pid, signal.SIGKILL)
                        except (ProcessLookupError, OSError):
                            pass  # Process already dead
        except Exception as e:
            print(f"Error stopping server: {e}", file=sys.stderr)
        finally:
            self.process = None
            # Also kill any orphaned processes on the port
            self._kill_port_processes()
            
            # Remove from active servers list
            if self._cleanup_registered and self in StreamableHTTPServer._active_servers:
                StreamableHTTPServer._active_servers.remove(self)
                self._cleanup_registered = False
    
    def _kill_port_processes(self) -> None:
        """Kill any processes using the server's port."""
        try:
            for proc in psutil.process_iter(['pid', 'connections']):
                try:
                    connections = proc.info.get('connections')
                    if connections:
                        for conn in connections:
                            if hasattr(conn, 'laddr') and conn.laddr.port == self.port:
                                proc.kill()
                                break
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
        except Exception as e:
            print(f"Error killing port processes: {e}", file=sys.stderr)
    
    def __enter__(self):
        self.start()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()
    
    @classmethod
    def cleanup_all(cls) -> None:
        """Clean up all active servers - called on exit."""
        for server in list(cls._active_servers):
            try:
                server.stop()
            except Exception as e:
                print(f"Error cleaning up server: {e}", file=sys.stderr)
        cls._active_servers.clear()


# Register cleanup handler for any uncaught exceptions or exits
atexit.register(StreamableHTTPServer.cleanup_all)


# Skip streamable-http if not available
TRANSPORTS = ["stdio"]
if HAS_STREAMABLE_HTTP:
    TRANSPORTS.append("streamable-http")

@pytest.fixture(params=TRANSPORTS)
async def mcp_session(request) -> AsyncGenerator[Tuple[ClientSession, str], None]:
    """Provide an MCP client session for testing with multiple transports.
    
    This fixture is parameterized to run tests with both STDIO and Streamable HTTP
    transports automatically. Includes bulletproof cleanup that guarantees
    all resources are released even if tests fail catastrophically.
    
    Args:
        request: pytest request object containing the transport parameter
        
    Yields:
        Tuple of (ClientSession, transport_name)
    """
    transport = request.param
    session = None
    cleanup_funcs = []
    server_instance = None  # Track server for guaranteed cleanup
    stdio_proc = None  # Track stdio subprocess
    
    # Register pytest finalizer for guaranteed cleanup
    def emergency_cleanup():
        """Emergency cleanup that runs no matter what."""
        # Clean up any streamable HTTP servers
        if server_instance:
            try:
                server_instance.stop()
            except Exception as e:
                print(f"Emergency cleanup of server failed: {e}", file=sys.stderr)
        
        # Clean up any stdio processes
        if stdio_proc:
            try:
                stdio_proc.terminate()
                stdio_proc.wait(timeout=2)
            except Exception:
                try:
                    stdio_proc.kill()
                except Exception:
                    pass
    
    request.addfinalizer(emergency_cleanup)
    
    try:
        if transport == "stdio":
            # Setup STDIO transport
            project_root = Path(__file__).parent.parent.parent
            server_module = "my_mcp_server.server.app"
            
            # Build environment with coverage support
            env = get_default_environment()
            
            # Add coverage-related environment variables if they exist
            coverage_vars = [
                "COVERAGE_PROCESS_START",
                "COVERAGE_FILE",
                "COVERAGE_CORE",
                "COV_CORE_SOURCE",
                "COV_CORE_CONFIG",
                "COV_CORE_DATAFILE",
            ]
            
            for var in coverage_vars:
                if var in os.environ:
                    env[var] = os.environ[var]
            
            # Add PYTHONPATH
            if "PYTHONPATH" in os.environ:
                env["PYTHONPATH"] = os.environ["PYTHONPATH"]
            else:
                env["PYTHONPATH"] = str(project_root)
            
            # Create server parameters
            server_params = StdioServerParameters(
                command=sys.executable,
                args=["-m", server_module, "--transport", "stdio"],
                env=env
            )
            
            # Start stdio client
            # Try with errlog parameter (SAAGA compatibility) then fallback
            import inspect
            sig = inspect.signature(stdio_client)
            if 'errlog' in sig.parameters:
                stdio_context = stdio_client(server_params, errlog=sys.stderr)
            else:
                stdio_context = stdio_client(server_params)
            read, write = await stdio_context.__aenter__()
            
            # Create and initialize session
            session = ClientSession(read, write)
            await session.__aenter__()
            await session.initialize()
            
            # Add cleanup for stdio
            async def cleanup_stdio():
                if session:
                    await session.__aexit__(None, None, None)
                await stdio_context.__aexit__(None, None, None)
            
            cleanup_funcs.append(cleanup_stdio)
            
        elif transport == "streamable-http":
            if not HAS_STREAMABLE_HTTP:
                pytest.skip("streamable_http module not available")
            
            # Setup Streamable HTTP transport
            port = 3001
            
            # Start server in subprocess
            server = StreamableHTTPServer(port)
            server_instance = server  # Track for emergency cleanup
            server.start()
            
            # Connect via Streamable HTTP
            url = f"http://localhost:{port}/mcp"
            http_context = streamablehttp_client(url)
            read, write, get_session_id = await http_context.__aenter__()
            
            # Create and initialize session
            session = ClientSession(read, write)
            await session.__aenter__()
            await session.initialize()
            
            # Store session ID for debugging
            session._streamable_session_id = get_session_id()
            
            # Add cleanup for streamable-http
            async def cleanup_http():
                try:
                    if session:
                        await session.__aexit__(None, None, None)
                except Exception as e:
                    print(f"Session cleanup error: {e}", file=sys.stderr)
                
                try:
                    await http_context.__aexit__(None, None, None)
                except Exception as e:
                    print(f"HTTP context cleanup error: {e}", file=sys.stderr)
                    
                try:
                    server.stop()
                except Exception as e:
                    print(f"Server stop error: {e}", file=sys.stderr)
            
            cleanup_funcs.append(cleanup_http)
        
        else:
            raise ValueError(f"Unknown transport: {transport}")
        
        # Yield the session and transport name
        yield session, transport
        
    finally:
        # Run all cleanup functions
        for cleanup_func in cleanup_funcs:
            try:
                await cleanup_func()
            except Exception as e:
                print(f"Cleanup error: {e}", file=sys.stderr)


@pytest.fixture
async def stdio_session() -> AsyncGenerator[ClientSession, None]:
    """Provide a STDIO-only MCP client session for specific tests.
    
    Use this fixture when you need to test STDIO-specific functionality.
    """
    async for session, transport in mcp_session(pytest.FixtureRequest(param="stdio")):
        if transport == "stdio":
            yield session


@pytest.fixture  
async def streamable_http_session() -> AsyncGenerator[ClientSession, None]:
    """Provide a Streamable HTTP-only MCP client session for specific tests.
    
    Use this fixture when you need to test Streamable HTTP-specific functionality.
    """
    async for session, transport in mcp_session(pytest.FixtureRequest(param="streamable-http")):
        if transport == "streamable-http":
            yield session


# Helper functions for tests

def extract_text_content(result) -> Optional[str]:
    """Extract text content from MCP tool result.
    
    Args:
        result: MCP CallToolResult
        
    Returns:
        Text content if found, None otherwise
    """
    from mcp import types
    
    for content in result.content:
        if isinstance(content, types.TextContent):
            return content.text
    return None


def extract_error_text(result) -> Optional[str]:
    """Extract error text from MCP error result.
    
    Args:
        result: MCP CallToolResult
        
    Returns:
        Error text if result is an error, None otherwise
    """
    if result.isError and result.content:
        return extract_text_content(result)
    return None