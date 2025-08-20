# AI Assistant Setup Guide - MCP Server Project

Quick setup instructions for AI assistants working with the MCP Server Project.

## Quick Setup Commands

### Installation
```bash
# Install as isolated tool (recommended)
uv tool install mcp_server_project

# Find binary location
which mcp_server_project-server  # macOS/Linux
where mcp_server_project-server  # Windows
```

### Development Setup
```bash
# Clone and setup for development
git clone <repository-url>
cd mcp_server_project

# Create virtual environment
uv venv
source venv/bin/activate  # Linux/macOS
# Or: venv\Scripts\activate  # Windows

# Install with all dependencies
uv pip install -e ".[ui,test,monitoring]"
```

## Key Commands to Know

### Server Commands
```bash
# Start server (stdio - default transport)
mcp_server_project-server

# Start with SSE transport
mcp_server_project-server --transport sse --port 3001

# Start with streamable HTTP transport
mcp_server_project-server --transport streamable-http --port 3001

# Get help
mcp_server_project-server --help
```

### Testing Commands
```bash
# Test client (stdio)
mcp_server_project-client "Hello, World!"

# Run all tests
pytest

# Run with coverage
pytest --cov=mcp_server_project

# Test correlation ID system
python test_correlation_id_integration.py

# Test unified logging
python test_unified_logging.py
```

### Development Tools
```bash
# MCP Inspector (for interactive testing)
PYTHONPATH=. mcp dev mcp_server_project/server/app.py

# Streamlit UI (monitoring interface)
streamlit run mcp_server_project/ui/app.py

# Code formatting
black mcp_server_project/
isort mcp_server_project/
```

## Important Files to Know

### Core Server Files
- **`server/app.py`**: Main MCP server with multi-transport support
- **`tools/echo.py`**: Simple echo tool (MCP TextContent)
- **`tools/example_tools.py`**: 10 comprehensive example tools
- **`client/app.py`**: Test client for development

### Configuration & Logging
- **`config.py`**: Runtime configuration management
- **`logging_config.py`**: OS-specific logging setup
- **`log_system/`**: Unified logging with SQLite backend and correlation IDs

### Advanced Features
- **`decorators/`**: 4 decorators (exception_handler, tool_logger, type_converter, parallelize)
- **`ui/`**: Streamlit web interface for monitoring
- **`tests/`**: Comprehensive test suite

### Configuration Files
- **`pyproject.toml`**: Package configuration with entry points
- **`test_*.py`**: Integration test files

## Available Tools (11 total)

### Basic Tools
- **echo**: Simple MCP TextContent echo with transforms
- **echo_tool**: Enhanced echo with structured response
- **get_time**: Current system time
- **random_number**: Random number generation with metadata

### Computation Tools
- **calculate_fibonacci**: Fibonacci calculation with performance metrics
- **search_tool**: Advanced search with configurable filters

### Interactive Tools
- **elicit_example**: User input elicitation demo
- **notification_example**: Logging and notification capabilities
- **progress_example**: Progress reporting demo

### Parallel Tools (Automatically Parallelized)
- **process_batch_data**: Batch text processing
- **simulate_heavy_computation**: CPU-intensive computation simulation

## Testing Workflow

### Quick Test
```bash
# 1. Test basic functionality
mcp_server_project-client "Hello, World!"

# 2. Test different transports
mcp_server_project-server --transport sse --port 3001 &
curl -X POST http://localhost:3001/tools/echo_tool \
  -H "Content-Type: application/json" \
  -d '{"message": "SSE Test"}'
kill %1  # Stop background server
```

### Comprehensive Testing
```bash
# 1. Unit and integration tests
pytest -v

# 2. Decorator system test
pytest tests/unit/test_decorators.py

# 3. Tool integration test
pytest tests/integration/test_example_tools_integration.py

# 4. Correlation ID tracking
python test_correlation_id_integration.py

# 5. Unified logging system
python test_unified_logging.py
```

### Interactive Testing
```bash
# MCP Inspector (web interface)
PYTHONPATH=. mcp dev mcp_server_project/server/app.py
# Access http://localhost:5173

# Streamlit monitoring UI
streamlit run mcp_server_project/ui/app.py
# Access http://localhost:8501
```

## Architecture Overview

### Transport Support
- **STDIO**: Default, for MCP clients like Claude Desktop
- **SSE**: Server-Sent Events for web clients
- **Streamable HTTP**: HTTP streaming for advanced clients

### Decorator Chain
1. **exception_handler**: Error handling and logging
2. **tool_logger**: Request logging with correlation IDs
3. **type_converter**: Parameter type conversion
4. **parallelize**: CPU-intensive task parallelization (select tools)

### Logging System
- **SQLite Backend**: Persistent structured logging
- **Correlation IDs**: Track requests across call chain
- **OS-specific Locations**: Platform-appropriate log directories
- **Automatic Rotation**: 10MB with 5 backups

### Web Interface
- **Home**: Server status and tool overview
- **Configuration**: Runtime config management
- **Logs**: Real-time log viewing with correlation tracking

## Common Debugging Commands

### Check Installation
```bash
# Verify server is installed
which mcp_server_project-server
mcp_server_project-server --help

# Check tools are registered
echo '{"method": "tools/list"}' | mcp_server_project-server
```

### Debug Logging
```bash
# Enable debug logging
export LOG_LEVEL=DEBUG
mcp_server_project-server

# View logs
tail -f ~/Library/Logs/mcp-servers/mcp_server_project.log  # macOS
tail -f ~/.local/state/mcp-servers/logs/mcp_server_project.log  # Linux
tail -f %LOCALAPPDATA%/mcp-servers/logs/mcp_server_project.log  # Windows
```

### Transport Debugging
```bash
# Test stdio (default)
echo '{"method": "ping"}' | mcp_server_project-server

# Test SSE
mcp_server_project-server --transport sse --port 3001 &
curl -s http://localhost:3001/health
kill %1

# Test streamable HTTP
mcp_server_project-server --transport streamable-http --port 3001 &
curl -s http://localhost:3001/mcp
kill %1
```

## Environment Variables

### Optional Configuration
- **LOG_LEVEL**: DEBUG, INFO, WARNING, ERROR (default: INFO)
- **MCP_SERVER_NAME**: Custom server name (default: "MCP Server Project")
- **MCP_SERVER_PORT**: Default port for SSE/HTTP (default: 3001)

### Development Variables
- **PYTHONPATH**: Set to "." when using MCP Inspector
- **MCP_DEBUG**: Enable additional debug output

## Important Notes

1. **No OAuth/Bazel/SAAGA**: This project doesn't use these technologies
2. **Python 3.11-3.12**: Required Python version range
3. **Cross-Platform**: Full Linux, macOS, Windows support
4. **Isolated Installation**: Use `uv tool install` to avoid conflicts
5. **Correlation Tracking**: All requests tracked with unique IDs
6. **Automatic Decoration**: Tools enhanced with decorators automatically

## Quick Development Checklist

When working with this project:

1. ✅ Install with `uv pip install -e ".[ui,test,monitoring]"`
2. ✅ Test with `mcp_server_project-client "test"`
3. ✅ Run pytest to ensure everything works
4. ✅ Use MCP Inspector for interactive tool testing
5. ✅ Check logs for correlation ID tracking
6. ✅ Test different transports if needed
7. ✅ Use Streamlit UI for monitoring

This setup guide should get you productive with the MCP Server Project quickly!