# ULTRA-DETAILED LINE-BY-LINE IMPLEMENTATION PLAN
## Port SAAGA MCP Cookie Cutter to Our Template

### SOURCE: https://github.com/SAGAAIDEV/saaga-mcp-server-cookie-cutter.git
### TARGET: /Users/timkitchens/projects/ai-projects/mcp-cookie-cutter

---

## PHASE 0: VERIFICATION & SETUP

### Step 0.1: Verify SAAGA Repository is Current
```
ACTION: Use code-understanding refresh_repo
SOURCE: https://github.com/SAGAAIDEV/saaga-mcp-server-cookie-cutter.git
VERIFY: Status shows "success" or "already current"
```

### Step 0.2: Verify Current State
```
ACTION: Check our current server/app.py
FILE: {{cookiecutter.__project_slug}}/{{cookiecutter.__project_slug}}/server/app.py
VERIFY: Line 8 shows "from mcp.server.fastmcp import FastMCP" (already using FastMCP)
VERIFY: Has register_tools() function starting around line 31
```

---

## PHASE 1: TOOLS (MUST BE DONE FIRST)

### Step 1.1: Get SAAGA's example_tools.py
```
ACTION: Read SAAGA file using code-understanding
SOURCE: example_server/example_server/tools/example_tools.py
TARGET: {{cookiecutter.__project_slug}}/{{cookiecutter.__project_slug}}/tools/example_tools.py
```

### Step 1.2: Create example_tools.py with ALL 10 Tools
```
ACTION: Write new file
FILE: {{cookiecutter.__project_slug}}/{{cookiecutter.__project_slug}}/tools/example_tools.py
CONTENT: Copy ENTIRE file from SAAGA INCLUDING:
  - Lines 1-14: Imports (MUST include "from mcp.server.fastmcp import Context")
  - Lines 15-28: echo_tool function
  - Lines 30-38: get_time function  
  - Lines 40-58: random_number function
  - Lines 60-90: calculate_fibonacci function
  - Lines 92-137: search_tool function (CRITICAL - has optional params)
  - Lines 139-145: BookingPreferences class (CRITICAL - Pydantic model)
  - Lines 147-164: elicit_example function (uses Context[ServerSession, None])
  - Lines 166-177: notification_example function
  - Lines 179-192: progress_example function
  - Lines 194-223: process_batch_data function
  - Lines 225-256: simulate_heavy_computation function
  - Lines 258-261: parallel_example_tools list = [process_batch_data, simulate_heavy_computation]
  - Lines 263-271: example_tools list = [echo_tool, get_time, random_number, calculate_fibonacci, search_tool, elicit_example, notification_example, progress_example]
  - Lines 273-285: get_tool_info function
  
VERIFY: File has exactly 10 tool functions + 1 helper + 1 model class
VERIFY: NO decorators on any tool function
VERIFY: All tools have ctx: Context parameter
```

### Step 1.3: Update tools/__init__.py
```
ACTION: Write file
FILE: {{cookiecutter.__project_slug}}/{{cookiecutter.__project_slug}}/tools/__init__.py
CONTENT:
from .example_tools import example_tools, parallel_example_tools

__all__ = ["example_tools", "parallel_example_tools"]

VERIFY: Only exports the two lists, not individual tools
```

---

## PHASE 2: DECORATORS (ALL 4 REQUIRED)

### Step 2.1: Create decorators directory
```
ACTION: Create directory
PATH: {{cookiecutter.__project_slug}}/{{cookiecutter.__project_slug}}/decorators/
```

### Step 2.2: Get exception_handler.py from SAAGA
```
ACTION: Read from SAAGA using code-understanding
SOURCE: {{cookiecutter.__project_slug}}/{{cookiecutter.__project_slug}}/decorators/exception_handler.py
TARGET: {{cookiecutter.__project_slug}}/{{cookiecutter.__project_slug}}/decorators/exception_handler.py
COPY: Entire file
VERIFY: Has exception_handler function that returns wrapper
```

### Step 2.3: Get tool_logger.py from SAAGA
```
ACTION: Read from SAAGA using code-understanding
SOURCE: {{cookiecutter.__project_slug}}/{{cookiecutter.__project_slug}}/decorators/tool_logger.py
TARGET: {{cookiecutter.__project_slug}}/{{cookiecutter.__project_slug}}/decorators/tool_logger.py
COPY: Entire file
VERIFY: Function signature has (func, config: dict = None)
VERIFY: Uses config parameter for logging settings
```

### Step 2.4: Get type_converter.py from SAAGA (CRITICAL!)
```
ACTION: Read from SAAGA using code-understanding
SOURCE: {{cookiecutter.__project_slug}}/{{cookiecutter.__project_slug}}/decorators/type_converter.py
TARGET: {{cookiecutter.__project_slug}}/{{cookiecutter.__project_slug}}/decorators/type_converter.py
COPY: Entire file
VERIFY: Handles conversion between MCP types and Python types
VERIFY: Has type_converter function
```

### Step 2.5: Get parallelize.py from SAAGA
```
ACTION: Read from SAAGA using code-understanding
SOURCE: {{cookiecutter.__project_slug}}/{{cookiecutter.__project_slug}}/decorators/parallelize.py
TARGET: {{cookiecutter.__project_slug}}/{{cookiecutter.__project_slug}}/decorators/parallelize.py
COPY: Entire file
VERIFY: Uses ThreadPoolExecutor
VERIFY: Has parallelize function that returns async wrapper
```

### Step 2.6: Create decorators/__init__.py
```
ACTION: Write file
FILE: {{cookiecutter.__project_slug}}/{{cookiecutter.__project_slug}}/decorators/__init__.py
CONTENT:
from .exception_handler import exception_handler
from .tool_logger import tool_logger
from .type_converter import type_converter
from .parallelize import parallelize

__all__ = ["exception_handler", "tool_logger", "type_converter", "parallelize"]

VERIFY: Exports all 4 decorators
```

---

## PHASE 3: SERVER ARCHITECTURE (CRITICAL SECTION)

### Step 3.1: Update server/app.py - Imports Section
```
ACTION: Read SAAGA's server/app.py
SOURCE: {{cookiecutter.__project_slug}}/{{cookiecutter.__project_slug}}/server/app.py (from SAAGA)
FOCUS: Lines 1-25 (imports section)

ACTION: Update our server/app.py imports
FILE: {{cookiecutter.__project_slug}}/{{cookiecutter.__project_slug}}/server/app.py
CHANGES:
  Line 6: Keep "import asyncio"
  Line 7: Keep "import sys"
  Line 8: Add "from typing import Optional, Callable, Any"
  Line 11: Keep "import click"
  Line 12: Keep "from mcp import types"
  Line 13: Keep "from mcp.server.fastmcp import FastMCP"
  Line 15-20: Update to:
    from {{ cookiecutter.__project_slug }}.config import ServerConfig, get_config
    from {{ cookiecutter.__project_slug }}.logging_config import setup_logging, logger
    from {{ cookiecutter.__project_slug }}.log_system.correlation import (
        generate_correlation_id,
        set_initialization_correlation_id,
        clear_initialization_correlation_id
    )
    from {{ cookiecutter.__project_slug }}.log_system.unified_logger import UnifiedLogger
    from {{ cookiecutter.__project_slug }}.tools.example_tools import example_tools, parallel_example_tools

VERIFY: Imports log_system not logging
VERIFY: Imports example_tools and parallel_example_tools lists
```

### Step 3.2: Update create_mcp_server function
```
ACTION: Replace create_mcp_server function
FILE: {{cookiecutter.__project_slug}}/{{cookiecutter.__project_slug}}/server/app.py
LOCATION: Lines 28-85 in SAAGA
COPY: Entire create_mcp_server function from SAAGA
EXCLUDE: Skip lines mentioning oauth_passthrough
KEY ELEMENTS:
  - Sets correlation ID before logging init
  - Initializes UnifiedLogger
  - Creates FastMCP instance
  - Calls register_tools(mcp_server, config)
  - Clears correlation ID after init

VERIFY: Function uses UnifiedLogger not traditional logging
VERIFY: Calls register_tools with config parameter
```

### Step 3.3: Update register_tools function (MOST CRITICAL)
```
ACTION: Replace entire register_tools function
FILE: {{cookiecutter.__project_slug}}/{{cookiecutter.__project_slug}}/server/app.py
SOURCE: SAAGA lines 91-147
CONTENT:
def register_tools(mcp_server: FastMCP, config: ServerConfig) -> None:
    """Register all MCP tools with the server using decorators."""
    
    # Get unified logger for registration logs
    import logging
    unified_logger = logging.getLogger('{{ cookiecutter.__project_slug }}')
    
    # Import decorators AT REGISTRATION TIME
    from {{ cookiecutter.__project_slug }}.decorators.exception_handler import exception_handler
    from {{ cookiecutter.__project_slug }}.decorators.tool_logger import tool_logger
    from {{ cookiecutter.__project_slug }}.decorators.type_converter import type_converter
    from {{ cookiecutter.__project_slug }}.decorators.parallelize import parallelize
    
    # Register regular tools with decorators
    for tool_func in example_tools:
        # Apply decorator chain: exception_handler → tool_logger → type_converter
        decorated_func = exception_handler(tool_logger(type_converter(tool_func), config.__dict__))
        
        # Extract metadata from the original function
        tool_name = tool_func.__name__
        
        # Register the decorated function directly with MCP
        mcp_server.tool(
            name=tool_name
        )(decorated_func)
        
        unified_logger.info(f"Registered tool: {tool_name}")
    
    # Register parallel tools with decorators  
    for tool_func in parallel_example_tools:
        # Apply decorator chain: exception_handler → tool_logger → parallelize(type_converter)
        decorated_func = exception_handler(tool_logger(parallelize(type_converter(tool_func)), config.__dict__))
        
        # Extract metadata
        tool_name = tool_func.__name__
        
        # Register directly with MCP
        mcp_server.tool(
            name=tool_name
        )(decorated_func)
        
        unified_logger.info(f"Registered parallel tool: {tool_name}")
    
    unified_logger.info(f"Server '{mcp_server.name}' initialized with decorators")

VERIFY: Decorators are applied AT REGISTRATION TIME
VERIFY: Regular tools: exception_handler(tool_logger(type_converter(tool_func), config.__dict__))
VERIFY: Parallel tools: exception_handler(tool_logger(parallelize(type_converter(tool_func)), config.__dict__))
VERIFY: NO OAuth section
```

### Step 3.4: Update main() function for 3 transports
```
ACTION: Replace main() function
FILE: {{cookiecutter.__project_slug}}/{{cookiecutter.__project_slug}}/server/app.py
SOURCE: SAAGA lines 165-214
KEY CHANGES:
  - Add streamable-http to transport choices
  - Add elif for streamable-http transport
  - Set streamable_http_path = "/mcp"
  
CONTENT:
@click.command()
@click.option(
    "--port",
    default={{ cookiecutter.server_port }},
    help="Port to listen on for SSE or Streamable HTTP transport"
)
@click.option(
    "--transport",
    type=click.Choice(["stdio", "sse", "streamable-http"]),
    default="stdio",
    help="Transport type (stdio, sse, or streamable-http)"
)
def main(port: int, transport: str) -> int:
    """Run the {{ cookiecutter.project_name }} server with specified transport."""
    async def run_server():
        """Inner async function to run the server and manage the event loop."""
        # Set the event loop in UnifiedLogger for async operations
        UnifiedLogger.set_event_loop(asyncio.get_running_loop())
        
        try:
            if transport == "stdio":
                logger.info("Starting server with STDIO transport")
                await server.run_stdio_async()
            elif transport == "sse":
                logger.info(f"Starting server with SSE transport on port {port}")
                server.settings.port = port
                await server.run_sse_async()
            elif transport == "streamable-http":
                logger.info(f"Starting server with Streamable HTTP transport on port {port}")
                server.settings.port = port
                server.settings.streamable_http_path = "/mcp"
                await server.run_streamable_http_async()
            else:
                raise ValueError(f"Unknown transport: {transport}")
        finally:
            # Clean up unified logger
            await UnifiedLogger.close()
    
    try:
        asyncio.run(run_server())
        return 0
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
        return 0
    except Exception as e:
        logger.error(f"Failed to start server: {e}", exc_info=True)
        return 1

VERIFY: Has all 3 transports in click.Choice
VERIFY: Has streamable-http elif block
VERIFY: Sets streamable_http_path = "/mcp"
```

### Step 3.5: Add convenience entry points
```
ACTION: Add after main() function
FILE: {{cookiecutter.__project_slug}}/{{cookiecutter.__project_slug}}/server/app.py
SOURCE: SAAGA lines 216-226
CONTENT:
def main_stdio() -> int:
    """Entry point for STDIO transport (convenience wrapper)."""
    return main.callback(port={{ cookiecutter.server_port }}, transport="stdio")

def main_http() -> int:
    """Entry point for Streamable HTTP transport (convenience wrapper)."""
    return main.callback(port={{ cookiecutter.server_port }}, transport="streamable-http")

def main_sse() -> int:
    """Entry point for SSE transport (convenience wrapper)."""
    return main.callback(port={{ cookiecutter.server_port }}, transport="sse")

VERIFY: All 3 convenience functions exist
```

---

## PHASE 4: LOG SYSTEM (NOT "logging")

### Step 4.1: Create log_system directory structure
```
ACTION: Create directories
PATHS:
  {{cookiecutter.__project_slug}}/{{cookiecutter.__project_slug}}/log_system/
  {{cookiecutter.__project_slug}}/{{cookiecutter.__project_slug}}/log_system/destinations/
```

### Step 4.2: Copy correlation.py
```
ACTION: Read from SAAGA and write
SOURCE: {{cookiecutter.__project_slug}}/{{cookiecutter.__project_slug}}/log_system/correlation.py
TARGET: {{cookiecutter.__project_slug}}/{{cookiecutter.__project_slug}}/log_system/correlation.py
COPY: Entire file
VERIFY: Has generate_correlation_id, set/get/clear functions
VERIFY: Has CorrelationContext class
```

### Step 4.3: Copy unified_logger.py
```
ACTION: Read from SAAGA and write
SOURCE: {{cookiecutter.__project_slug}}/{{cookiecutter.__project_slug}}/log_system/unified_logger.py
TARGET: {{cookiecutter.__project_slug}}/{{cookiecutter.__project_slug}}/log_system/unified_logger.py
COPY: Entire file
VERIFY: Has UnifiedLogger class
VERIFY: Has initialize_from_config and initialize_default methods
```

### Step 4.4: Copy destinations/base.py
```
ACTION: Read from SAAGA and write
SOURCE: {{cookiecutter.__project_slug}}/{{cookiecutter.__project_slug}}/log_system/destinations/base.py
TARGET: {{cookiecutter.__project_slug}}/{{cookiecutter.__project_slug}}/log_system/destinations/base.py
COPY: Entire file
VERIFY: Has LogDestination abstract base class
```

### Step 4.5: Copy destinations/sqlite.py
```
ACTION: Read from SAAGA and write
SOURCE: {{cookiecutter.__project_slug}}/{{cookiecutter.__project_slug}}/log_system/destinations/sqlite.py
TARGET: {{cookiecutter.__project_slug}}/{{cookiecutter.__project_slug}}/log_system/destinations/sqlite.py
COPY: Entire file
VERIFY: Has SQLiteDestination class
```

### Step 4.6: Copy destinations/factory.py
```
ACTION: Read from SAAGA and write
SOURCE: {{cookiecutter.__project_slug}}/{{cookiecutter.__project_slug}}/log_system/destinations/factory.py
TARGET: {{cookiecutter.__project_slug}}/{{cookiecutter.__project_slug}}/log_system/destinations/factory.py
COPY: Entire file
EXCLUDE: Remove any OAuth or SAAGA-specific destination types
VERIFY: Has DestinationFactory class
```

### Step 4.7: Create destinations/__init__.py
```
ACTION: Write file
FILE: {{cookiecutter.__project_slug}}/{{cookiecutter.__project_slug}}/log_system/destinations/__init__.py
CONTENT:
from .base import LogDestination, LogEntry, DestinationConfig
from .sqlite import SQLiteDestination
from .factory import DestinationFactory

__all__ = ["LogDestination", "LogEntry", "DestinationConfig", "SQLiteDestination", "DestinationFactory"]
```

### Step 4.8: Create log_system/__init__.py
```
ACTION: Write file
FILE: {{cookiecutter.__project_slug}}/{{cookiecutter.__project_slug}}/log_system/__init__.py
CONTENT:
from .correlation import generate_correlation_id, set_correlation_id, get_correlation_id, clear_correlation_id
from .unified_logger import UnifiedLogger

__all__ = [
    "generate_correlation_id",
    "set_correlation_id", 
    "get_correlation_id",
    "clear_correlation_id",
    "UnifiedLogger"
]
```

---

## PHASE 5: UPDATE CONFIGURATION

### Step 5.1: Update config.py
```
ACTION: Read SAAGA's config.py
SOURCE: {{cookiecutter.__project_slug}}/{{cookiecutter.__project_slug}}/config.py
TARGET: {{cookiecutter.__project_slug}}/{{cookiecutter.__project_slug}}/config.py
KEY ADDITIONS:
  - Add logging_destinations field
  - Add get_config() function
  - Use dataclass with platform-aware paths
VERIFY: Has ServerConfig dataclass
VERIFY: Has get_config() function
```

### Step 5.2: Update pyproject.toml dependencies
```
ACTION: Edit file
FILE: {{cookiecutter.__project_slug}}/pyproject.toml
ADD to dependencies:
  - "pydantic>=2.0.0"
  - "pydantic-settings>=2.0.0"
  - "platformdirs>=4.0.0"
  - "python-dotenv>=1.0.0"
  - "click>=8.0.0"
ADD to optional-dependencies:
  [project.optional-dependencies]
  monitoring = ["psutil>=5.9.0"]
  ui = ["streamlit>=1.29.0"]
ADD to scripts:
  {{ cookiecutter.__project_slug }}-server-stdio = "{{ cookiecutter.__project_slug }}.server.app:main_stdio"
  {{ cookiecutter.__project_slug }}-server-http = "{{ cookiecutter.__project_slug }}.server.app:main_http"
  {{ cookiecutter.__project_slug }}-server-sse = "{{ cookiecutter.__project_slug }}.server.app:main_sse"
```

---

## PHASE 6: STREAMLIT UI (Large Section)

### Step 6.1: Create UI directory structure
```
ACTION: Create directories
PATHS:
  {{cookiecutter.__project_slug}}/{{cookiecutter.__project_slug}}/ui/
  {{cookiecutter.__project_slug}}/{{cookiecutter.__project_slug}}/ui/pages/
  {{cookiecutter.__project_slug}}/{{cookiecutter.__project_slug}}/ui/lib/
```

### Step 6.2: Copy ui/app.py
```
ACTION: Read from SAAGA and write
SOURCE: {{cookiecutter.__project_slug}}/{{cookiecutter.__project_slug}}/ui/app.py
TARGET: {{cookiecutter.__project_slug}}/{{cookiecutter.__project_slug}}/ui/app.py
COPY: Entire file
REPLACE: "SAAGA" with "{{ cookiecutter.project_name }}"
```

### Step 6.3: Copy UI pages
```
ACTION: Copy each page file
FILES:
  ui/pages/1_Home.py
  ui/pages/2_Configuration.py
  ui/pages/3_Logs.py
REPLACE: "SAAGA" branding with generic terms
```

### Step 6.4: Copy UI lib files
```
ACTION: Copy each lib file
FILES:
  ui/lib/components.py
  ui/lib/styles.py
  ui/lib/utils.py
```

---

## PHASE 7: TESTS

### Step 7.1: Create test directory structure
```
ACTION: Create directories
PATHS:
  {{cookiecutter.__project_slug}}/tests/
  {{cookiecutter.__project_slug}}/tests/unit/
  {{cookiecutter.__project_slug}}/tests/integration/
```

### Step 7.2: Copy test files
```
ACTION: Copy test files from SAAGA
EXCLUDE: Tests that reference OAuth
FILES:
  tests/conftest.py
  tests/unit/test_decorators.py
  tests/unit/test_tools.py (if exists)
  tests/integration/test_server.py (if exists)
```

---

## PHASE 8: CLAUDE COMMANDS & REFERENCE

### Step 8.1: Create .claude directory
```
ACTION: Create directory
PATH: {{cookiecutter.__project_slug}}/.claude/
```

### Step 8.2: Add Your 4 Custom Claude Commands
```
ACTION: Write file
FILE: {{cookiecutter.__project_slug}}/.claude/mcp_commands.md
CONTENT: [THE 4 CUSTOM COMMANDS YOU PROVIDED - NEED YOU TO SPECIFY THESE]
NOTE: You mentioned 4 specific Claude commands to include - please provide them
```

### Step 8.3: Copy .reference directory structure
```
ACTION: Read SAAGA's .reference directory
SOURCE: .reference/
VERIFY: Check what subdirectories and files exist
```

### Step 8.4: Copy .reference/patterns/
```
ACTION: Copy directory
SOURCE: .reference/patterns/
TARGET: .reference/patterns/
FILES TO INCLUDE:
  - decorator_patterns.py
  - tool_patterns.py
  - integration_test_patterns.py
  - unit_test_patterns.py
EXCLUDE: OAuth patterns, Bazel patterns
REPLACE: SAAGA references with generic
```

### Step 8.5: Copy .reference/examples/
```
ACTION: Copy directory if exists
SOURCE: .reference/examples/
TARGET: .reference/examples/
EXCLUDE: OAuth examples
```

### Step 8.6: Copy .reference/README.md
```
ACTION: Copy and modify
SOURCE: .reference/README.md
TARGET: .reference/README.md
REPLACE: SAAGA branding with generic documentation
```

### Step 8.7: Update cookiecutter.json
```
ACTION: Read SAAGA's cookiecutter.json
SOURCE: cookiecutter.json
TARGET: cookiecutter.json
VERIFY: Has all necessary template variables:
  - project_name
  - project_slug
  - description
  - author_name
  - author_email
  - server_port (default 3001)
  - include_example_tools (default "yes")
  - include_parallel_example (default "yes")
  - default_transport (default "stdio")
EXCLUDE: OAuth-related options
```

### Step 8.8: Update hooks/pre_gen_project.py
```
ACTION: Copy from SAAGA
SOURCE: hooks/pre_gen_project.py
TARGET: hooks/pre_gen_project.py
CONTENT: Validation logic for cookiecutter variables
VERIFY: Validates project_slug format
```

### Step 8.9: Update hooks/post_gen_project.py
```
ACTION: Copy from SAAGA
SOURCE: hooks/post_gen_project.py
TARGET: hooks/post_gen_project.py
KEY FEATURES:
  - Creates virtual environment automatically
  - Installs dependencies with uv or pip
  - Creates .env file with defaults
  - Shows helpful next steps message
VERIFY: Has create_virtualenv() function
VERIFY: Has install_dependencies() function
```

---

## PHASE 9: ADDITIONAL MISSING COMPONENTS

### Step 9.1: Create example_server directory (for testing)
```
ACTION: Note this is generated by cookiecutter
PATH: example_server/ (will be created when testing)
PURPOSE: This is where we test the generated server
```

### Step 9.2: Copy correlation ID test script
```
ACTION: Read from SAAGA
SOURCE: test_correlation_id_integration.py (if exists at root)
TARGET: test_correlation_id_integration.py
PURPOSE: Tests correlation ID tracking across tool calls
```

### Step 9.3: Create .env.example file
```
ACTION: Write file
FILE: {{cookiecutter.__project_slug}}/.env.example
CONTENT:
# {{ cookiecutter.project_name }} Configuration
LOG_LEVEL=INFO
SERVER_PORT={{ cookiecutter.server_port }}
DEBUG=false
ENABLE_METRICS=true
```

### Step 9.4: Update README.md template
```
ACTION: Update template README
FILE: {{cookiecutter.__project_slug}}/README.md
INCLUDE:
  - All 3 transport examples
  - List of all 10 tools
  - Installation instructions
  - Testing instructions
  - Streamlit UI instructions
```

### Step 9.5: Create DEVELOPMENT.md
```
ACTION: Copy from SAAGA and modify
SOURCE: {{cookiecutter.__project_slug}}/DEVELOPMENT.md
TARGET: {{cookiecutter.__project_slug}}/DEVELOPMENT.md
CONTENT:
  - How to add new tools
  - Decorator pattern explanation
  - Testing guidelines
  - Contribution guidelines
EXCLUDE: OAuth development, Bazel instructions
```

---

## PHASE 10: FINAL VERIFICATION

### Step 10.1: Verify No OAuth References
```
ACTION: Search all files
SEARCH FOR: "oauth", "OAuth", "passthrough"
VERIFY: No matches except in comments explaining exclusion
```

### Step 9.2: Verify No Bazel References
```
ACTION: Search all files
SEARCH FOR: "bazel", "BUILD", "WORKSPACE"
VERIFY: No matches
```

### Step 9.3: Verify No SAAGA Branding
```
ACTION: Search all files
SEARCH FOR: "SAAGA", "saaga"
VERIFY: No matches except in comments
```

### Step 9.4: Generate Test Server
```
ACTION: Run cookiecutter
COMMAND: cookiecutter . --no-input
VERIFY: Server generates without errors
```

### Step 9.5: Test All Tools
```
ACTION: Start server and test each tool
VERIFY: All 10 tools are registered
VERIFY: echo_tool, get_time, random_number, calculate_fibonacci work
VERIFY: search_tool handles optional parameters
VERIFY: elicit_example, notification_example, progress_example work with Context
VERIFY: process_batch_data, simulate_heavy_computation run in parallel
```

### Step 9.6: Test All Transports
```
ACTION: Test each transport
COMMANDS:
  server --transport stdio
  server --transport sse --port 3001
  server --transport streamable-http --port 3001
VERIFY: All 3 transports start successfully
```

---

## CRITICAL REMINDERS

1. **NEVER** apply decorators in tool definitions - only at registration
2. **ALWAYS** use log_system/ not logging/
3. **MUST** include type_converter decorator
4. **MUST** support all 3 transports including streamable-http
5. **NO** OAuth code anywhere
6. **NO** Bazel files
7. **NO** SAAGA branding

## ERROR RECOVERY

If any step fails:
1. Check if trying to copy OAuth-related code
2. Verify source file exists in SAAGA
3. Check for import errors (especially Context from fastmcp)
4. Verify decorator chain order is correct
5. Ensure log_system paths are used not logging

## SUCCESS CRITERIA

✓ All 10 tools work
✓ All 3 transports work
✓ Decorators applied at registration
✓ Type converter included
✓ Unified logging works
✓ Correlation IDs tracked
✓ Streamlit UI functional
✓ No OAuth/Bazel/SAAGA references