# {{cookiecutter.project_name}} - Quick Setup Guide

Quick setup instructions for using this MCP server with AI assistants.

## Quick Setup Commands

### Installation
```bash
# Install as isolated tool (recommended)
uv tool install {{cookiecutter.project_slug}}

# Find binary location
which {{cookiecutter.project_slug}}-server  # macOS/Linux
where {{cookiecutter.project_slug}}-server  # Windows
```

### Development Setup
```bash
# Clone and setup for development
git clone <repository-url>
cd {{cookiecutter.project_slug}}

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
{{cookiecutter.project_slug}}-server

# Start with SSE transport
{{cookiecutter.project_slug}}-server --transport sse --port 3001

# Start with streamable HTTP transport
{{cookiecutter.project_slug}}-server --transport streamable-http --port 3001

# Get help
{{cookiecutter.project_slug}}-server --help
```

### Testing Commands
```bash
# Test client (stdio)
{{cookiecutter.project_slug}}-client "Hello, World!"

# Run all tests
pytest

# Run with coverage
pytest --cov={{cookiecutter.project_slug}}

# Test correlation ID system
python test_correlation_id_integration.py

# Test unified logging
python test_unified_logging.py
```

### Development Tools
```bash
# MCP Inspector (for interactive testing)
PYTHONPATH=. mcp dev {{cookiecutter.project_slug}}/server/app.py

# Streamlit UI (monitoring interface)
streamlit run {{cookiecutter.project_slug}}/ui/app.py

# Code formatting
black {{cookiecutter.project_slug}}/
isort {{cookiecutter.project_slug}}/
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
{{cookiecutter.project_slug}}-client "Hello, World!"

# 2. Test different transports
{{cookiecutter.project_slug}}-server --transport sse --port 3001 &
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
PYTHONPATH=. mcp dev {{cookiecutter.project_slug}}/server/app.py
# Access http://localhost:5173

# Streamlit monitoring UI
streamlit run {{cookiecutter.project_slug}}/ui/app.py
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
which {{cookiecutter.project_slug}}-server
{{cookiecutter.project_slug}}-server --help

# Check tools are registered
echo '{"method": "tools/list"}' | {{cookiecutter.project_slug}}-server
```

### Debug Logging
```bash
# Enable debug logging
export LOG_LEVEL=DEBUG
{{cookiecutter.project_slug}}-server

# View logs
tail -f ~/Library/Logs/mcp-servers/{{cookiecutter.project_slug}}.log  # macOS
tail -f ~/.local/state/mcp-servers/logs/{{cookiecutter.project_slug}}.log  # Linux
tail -f %LOCALAPPDATA%/mcp-servers/logs/{{cookiecutter.project_slug}}.log  # Windows
```

### Transport Debugging
```bash
# Test stdio (default)
echo '{"method": "ping"}' | {{cookiecutter.project_slug}}-server

# Test SSE
{{cookiecutter.project_slug}}-server --transport sse --port 3001 &
curl -s http://localhost:3001/health
kill %1

# Test streamable HTTP
{{cookiecutter.project_slug}}-server --transport streamable-http --port 3001 &
curl -s http://localhost:3001/mcp
kill %1
```

## Environment Variables

### Optional Configuration
- **LOG_LEVEL**: DEBUG, INFO, WARNING, ERROR (default: INFO)
- **MCP_SERVER_NAME**: Custom server name (default: "{{cookiecutter.project_name}}")
- **MCP_SERVER_PORT**: Default port for SSE/HTTP (default: 3001)

### Development Variables
- **PYTHONPATH**: Set to "." when using MCP Inspector
- **MCP_DEBUG**: Enable additional debug output

## Important Notes

1. **Python {{cookiecutter.python_version}}+**: Required Python version
2. **Cross-Platform**: Full Linux, macOS, Windows support
3. **Isolated Installation**: Use `uv tool install` to avoid conflicts
4. **Correlation Tracking**: All requests tracked with unique IDs
5. **Automatic Decoration**: Tools enhanced with decorators automatically

## Quick Development Checklist

When working with this project:

1. ✅ Install with `uv pip install -e ".[ui,test,monitoring]"`
2. ✅ Test with `{{cookiecutter.project_slug}}-client "test"`
3. ✅ Run pytest to ensure everything works
4. ✅ Use MCP Inspector for interactive tool testing
5. ✅ Check logs for correlation ID tracking
6. ✅ Test different transports if needed
7. ✅ Use Streamlit UI for monitoring

This setup guide should get you productive with {{cookiecutter.project_name}} quickly!