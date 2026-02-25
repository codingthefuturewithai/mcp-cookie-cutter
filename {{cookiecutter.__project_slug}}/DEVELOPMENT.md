# Development Guide

This guide covers development practices, architecture, and contribution guidelines for the MCP Server Project.

## Development Setup

### Prerequisites

- Python 3.11-3.12
- uv (recommended) or pip
- Git for version control
- Docker (optional, for containerized deployment)

### Initial Setup

1. **Clone and create virtual environment:**

   ```bash
   git clone <repository-url>
   cd {{ cookiecutter.__project_slug }}

   # Create and activate virtual environment
   uv venv
   source venv/bin/activate  # Linux/macOS
   # Or: venv\Scripts\activate  # Windows
   ```

2. **Install in development mode:**

   ```bash
   # Install with all optional dependencies
   uv pip install -e ".[ui,test,monitoring]"

   # Or install just core dependencies
   uv pip install -e .
   ```

3. **Verify installation:**

   ```bash
   # Test the server
   {{ cookiecutter.__project_slug }}-server --help

   # Test the client
   {{ cookiecutter.__project_slug }}-client "Hello, World!"

   # Test different transports
   {{ cookiecutter.__project_slug }}-server --transport stdio
   {{ cookiecutter.__project_slug }}-server --transport sse --port 3001
   {{ cookiecutter.__project_slug }}-server --transport streamable-http --port 3001
   ```

### Development Dependencies

Install additional development tools:

```bash
# Code formatting and linting
uv pip install black isort flake8 mypy

# Pre-commit hooks (optional)
uv pip install pre-commit
pre-commit install
```

## Architecture Overview

The MCP Server Project is built with a modular architecture featuring:

### Core Components

- **Server (`server/app.py`)**: Main MCP server with multi-transport support
- **Tools (`tools/`)**: Individual tool implementations
- **Decorators (`decorators/`)**: Function decorators for cross-cutting concerns
- **Log System (`log_system/`)**: Unified logging with correlation tracking
- **UI (`ui/`)**: Streamlit-based web interface
- **Client (`client/app.py`)**: Test client for development

### Project Structure

```
{{ cookiecutter.__project_slug }}/
├── {{ cookiecutter.__project_slug }}/           # Main package
│   ├── __init__.py
│   ├── config.py                 # Configuration management
│   ├── logging_config.py         # OS-specific logging setup
│   │
│   ├── server/                   # MCP server implementation
│   │   ├── __init__.py
│   │   └── app.py               # Main server with multi-transport
│   │
│   ├── client/                   # Test client
│   │   ├── __init__.py
│   │   └── app.py               # STDIO test client
│   │
│   ├── tools/                    # Tool implementations
│   │   ├── __init__.py
│   │   ├── echo.py              # Simple echo tool
│   │   └── example_tools.py     # Comprehensive tool examples
│   │
│   ├── decorators/               # Function decorators
│   │   ├── __init__.py
│   │   ├── exception_handler.py  # Error handling
│   │   ├── tool_logger.py       # Request logging
│   │   ├── type_converter.py    # Parameter conversion
│   │   └── parallelize.py       # Async parallelization
│   │
│   ├── log_system/              # Unified logging system
│   │   ├── __init__.py
│   │   ├── correlation.py       # Correlation ID management
│   │   ├── unified_logger.py    # Main logger interface
│   │   └── destinations/        # Log destinations
│   │       ├── __init__.py
│   │       ├── base.py          # Base destination class
│   │       ├── factory.py       # Destination factory
│   │       └── sqlite.py        # SQLite log destination
│   │
│   └── ui/                      # Streamlit web interface
│       ├── __init__.py
│       ├── app.py               # Main Streamlit app
│       ├── lib/                 # UI utilities
│       │   ├── __init__.py
│       │   ├── components.py    # Reusable components
│       │   ├── styles.py        # CSS styling
│       │   └── utils.py         # Utility functions
│       └── pages/               # Streamlit pages
│           ├── 1_Home.py        # Server overview
│           ├── 2_Configuration.py # Config management
│           └── 3_Logs.py        # Log viewing
│
├── tests/                       # Test suite
│   ├── __init__.py
│   ├── conftest.py              # Pytest configuration
│   ├── unit/                    # Unit tests
│   │   ├── __init__.py
│   │   └── test_decorators.py   # Decorator tests
│   └── integration/             # Integration tests
│       ├── __init__.py
│       ├── conftest.py
│       └── test_example_tools_integration.py
│
├── test_correlation_id_integration.py  # Correlation ID test
├── test_unified_logging.py            # Logging system test
├── pyproject.toml                     # Package configuration
├── Dockerfile                         # Docker container build
├── docker-compose.yml                 # Docker Compose configuration
├── scripts/
│   └── docker.py                      # Docker management script
├── README.md                          # User documentation
└── DEVELOPMENT.md                     # This file
```

### Design Patterns

#### 1. Decorator Pattern

All tools are automatically decorated with:

- **Exception Handler**: Catches and logs errors
- **Tool Logger**: Logs calls with correlation IDs
- **Type Converter**: Ensures proper parameter types
- **Parallelize**: Parallelizes compute-intensive tools

#### 2. Factory Pattern

Log destinations use a factory pattern for flexibility:

```python
from {{ cookiecutter.__project_slug }}.log_system.destinations.factory import create_destination

# Creates appropriate destination based on type
destination = create_destination("sqlite", settings)
```

#### 3. Correlation ID Pattern

All requests are tracked with unique correlation IDs:

- Generated at request entry
- Passed through the entire call chain
- Logged with all operations
- Used for distributed tracing

## Adding New Tools

### Basic Tool Structure

1. **Create tool function:**

   ```python
   # tools/my_tool.py
   import logging
   from typing import Dict, Any
   from fastmcp import Context

   logger = logging.getLogger(__name__)

   async def my_tool(param1: str, param2: int = 10, ctx: Context = None) -> Dict[str, Any]:
       """My custom tool implementation.

       Args:
           param1: Description of first parameter
           param2: Description of second parameter (optional)
           ctx: MCP Context (automatically provided)

       Returns:
           Dictionary with results
       """
       logger.info(f"Processing {param1} with {param2}")

       # Your logic here
       result = process_data(param1, param2)

       return {
           "input": param1,
           "multiplier": param2,
           "result": result,
           "timestamp": time.time()
       }
   ```

2. **Register tool in server:**

   ```python
   # server/app.py
   from {{ cookiecutter.__project_slug }}.tools.my_tool import my_tool

   # Add to appropriate list
   example_tools = [
       # ... existing tools
       my_tool,
   ]
   ```

### Tool Types

#### Regular Tools

For most tools, add to `example_tools` list:

```python
example_tools = [
    echo_tool,
    get_time,
    my_new_tool,  # Add here
]
```

#### Parallel Tools

For compute-intensive tools, add to `parallel_example_tools`:

```python
parallel_example_tools = [
    process_batch_data,
    simulate_heavy_computation,
    my_heavy_tool,  # Add here
]
```

### Tool Guidelines

1. **Always include type hints**
2. **Use descriptive docstrings**
3. **Include Context parameter for advanced features**
4. **Log important operations**
5. **Handle errors gracefully**
6. **Return structured data when possible**

### MCP Context Features

The `Context` parameter provides access to MCP features:

```python
async def advanced_tool(data: str, ctx: Context = None) -> str:
    # Progress reporting
    await ctx.report_progress(progress=0.5, message="Halfway done")

    # Logging at different levels
    await ctx.debug("Debug information")
    await ctx.info("Processing started")
    await ctx.warning("This might take a while")
    await ctx.error("Something went wrong")

    # User interaction (elicit input)
    result = await ctx.elicit(
        message="Choose an option:",
        schema=MySchema
    )

    # Resource notifications
    await ctx.send_notification(mcp.types.ResourceListChangedNotification())

    return "Processing complete"
```

## Decorator System Explained

### Exception Handler

```python
# decorators/exception_handler.py
def exception_handler(func):
    """Catches exceptions and returns user-friendly errors."""
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except Exception as e:
            logger.error(f"Tool error: {e}")
            return {"error": str(e), "type": type(e).__name__}
    return wrapper
```

### Tool Logger

```python
# decorators/tool_logger.py
def tool_logger(func, config):
    """Logs all tool calls with correlation IDs."""
    async def wrapper(*args, **kwargs):
        correlation_id = get_correlation_id()
        logger.info(f"[{correlation_id}] Calling {func.__name__}")

        start_time = time.time()
        result = await func(*args, **kwargs)
        duration = time.time() - start_time

        logger.info(f"[{correlation_id}] {func.__name__} completed in {duration:.3f}s")
        return result
    return wrapper
```

### Type Converter

```python
# decorators/type_converter.py
def type_converter(func):
    """Ensures parameters have correct types."""
    async def wrapper(*args, **kwargs):
        # Convert parameters based on function signature
        converted_kwargs = convert_types(func, kwargs)
        return await func(*args, **converted_kwargs)
    return wrapper
```

### Parallelize

```python
# decorators/parallelize.py
def parallelize(func):
    """Runs function in thread pool for CPU-intensive tasks."""
    async def wrapper(*args, **kwargs):
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, func, *args, **kwargs)
    return wrapper
```

## Testing Guidelines

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov={{ cookiecutter.__project_slug }}

# Run specific test types
pytest tests/unit/
pytest tests/integration/

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/unit/test_decorators.py

# Run correlation ID test
python test_correlation_id_integration.py

# Run logging system test
python test_unified_logging.py
```

### Writing Tests

#### Unit Tests

```python
# tests/unit/test_my_tool.py
import pytest
from {{ cookiecutter.__project_slug }}.tools.my_tool import my_tool

@pytest.mark.asyncio
async def test_my_tool_basic():
    """Test basic functionality."""
    result = await my_tool("test", 5)

    assert result["input"] == "test"
    assert result["multiplier"] == 5
    assert "result" in result
    assert "timestamp" in result

@pytest.mark.asyncio
async def test_my_tool_defaults():
    """Test default parameters."""
    result = await my_tool("test")  # param2 should default to 10

    assert result["multiplier"] == 10
```

#### Integration Tests

```python
# tests/integration/test_my_tool_integration.py
import pytest
from {{ cookiecutter.__project_slug }}.server.app import create_mcp_server

@pytest.mark.asyncio
async def test_tool_through_server():
    """Test tool through MCP server."""
    server = create_mcp_server()

    # Test tool registration
    assert "my_tool" in server.list_tools()

    # Test tool execution
    result = await server.call_tool("my_tool", {"param1": "test"})
    assert result is not None
```

### Test Configuration

```python
# tests/conftest.py
import pytest
from {{ cookiecutter.__project_slug }}.config import ServerConfig

@pytest.fixture
def test_config():
    """Test configuration."""
    return ServerConfig(
        name="Test Server",
        log_level="DEBUG",
        port=3002  # Use different port for tests
    )

@pytest.fixture
def mock_context():
    """Mock MCP context for testing."""
    # Create mock context implementation
    pass
```

## Contribution Guidelines

### Code Standards

1. **Follow PEP 8** style guidelines
2. **Use type hints** for all functions
3. **Write descriptive docstrings** (Google style)
4. **Keep functions focused** (single responsibility)
5. **Handle errors gracefully**
6. **Add tests** for new functionality

### Code Formatting

```bash
# Format code
black {{ cookiecutter.__project_slug }}/
isort {{ cookiecutter.__project_slug }}/

# Check formatting
black --check {{ cookiecutter.__project_slug }}/
isort --check-only {{ cookiecutter.__project_slug }}/

# Lint code
flake8 {{ cookiecutter.__project_slug }}/
mypy {{ cookiecutter.__project_slug }}/
```

### Git Workflow

1. **Create feature branch:**

   ```bash
   git checkout -b feature/my-new-tool
   ```

2. **Make changes with good commit messages:**

   ```bash
   git add .
   git commit -m "feat: add my_new_tool with batch processing"
   ```

3. **Run tests:**

   ```bash
   pytest
   python test_correlation_id_integration.py
   python test_unified_logging.py
   ```

4. **Push and create PR:**
   ```bash
   git push origin feature/my-new-tool
   # Create Pull Request on GitHub/GitLab
   ```

### Commit Message Format

Use conventional commit format:

- `feat:` new features
- `fix:` bug fixes
- `docs:` documentation changes
- `test:` adding tests
- `refactor:` code refactoring
- `style:` formatting changes
- `chore:` maintenance tasks

### Pull Request Guidelines

1. **Include clear description** of changes
2. **Add tests** for new functionality
3. **Update documentation** as needed
4. **Ensure all tests pass**
5. **Follow code style guidelines**
6. **Keep PRs focused** (one feature per PR)

## Debugging and Development Tools

### MCP Inspector

```bash
# Install package first
uv pip install -e .

# Start MCP Inspector
PYTHONPATH=. mcp dev {{ cookiecutter.__project_slug }}/server/app.py
```

Access at http://localhost:5173 to:

- Test tools interactively
- View tool parameters and responses
- Debug tool execution

### Streamlit UI

```bash
# Install UI dependencies
uv pip install -e ".[ui]"

# Start Streamlit interface
streamlit run {{ cookiecutter.__project_slug }}/ui/app.py
```

Features:

- Server status monitoring
- Configuration management
- Real-time log viewing
- Correlation ID tracking

### Manual Testing

```bash
# Test different transports
{{ cookiecutter.__project_slug }}-server --transport stdio
{{ cookiecutter.__project_slug }}-server --transport sse --port 3001
{{ cookiecutter.__project_slug }}-server --transport streamable-http --port 3001

# Test client
{{ cookiecutter.__project_slug }}-client "Hello, World!"

# Test with curl (SSE transport)
curl -X POST http://localhost:3001/tools/echo \
  -H "Content-Type: application/json" \
  -d '{"text": "Hello SSE"}'
```

### Docker Testing

Run the server in a Docker container for isolated, production-like testing:

```bash
# Build and start container
python scripts/docker.py start

# Check status
python scripts/docker.py status

# View logs
python scripts/docker.py logs

# Rebuild after code changes
python scripts/docker.py update

# Stop container
python scripts/docker.py stop
```

The container exposes the MCP endpoint at `http://localhost:<port>/mcp` using streamable-http transport. See [README.md](README.md#docker-deployment) for full details.

### Logging and Debugging

```bash
# Set debug logging
export LOG_LEVEL=DEBUG
{{ cookiecutter.__project_slug }}-server

# View logs
tail -f ~/.local/state/mcp-servers/logs/{{ cookiecutter.__project_slug }}.log  # Linux
tail -f ~/Library/Logs/mcp-servers/{{ cookiecutter.__project_slug }}.log       # macOS

# Test correlation ID tracking
python test_correlation_id_integration.py

# Test unified logging
python test_unified_logging.py
```

## Performance Considerations

### Parallel Tools

Use parallelization for:

- CPU-intensive computations
- Batch processing operations
- Long-running calculations

```python
# Add to parallel_example_tools for automatic parallelization
parallel_example_tools = [
    my_heavy_computation,
    batch_processor,
]
```

### Async Best Practices

1. **Use async/await** for I/O operations
2. **Avoid blocking calls** in async functions
3. **Use asyncio.sleep()** instead of time.sleep()
4. **Handle cancellation** properly

```python
async def async_tool(data: str, ctx: Context = None) -> Dict[str, Any]:
    # Good: async I/O
    async with aiofiles.open('file.txt', 'r') as f:
        content = await f.read()

    # Good: yielding control
    await asyncio.sleep(0.1)  # Not time.sleep(0.1)

    # Good: async HTTP requests
    async with aiohttp.ClientSession() as session:
        async with session.get('https://api.example.com') as response:
            data = await response.json()

    return {"result": data}
```

## Troubleshooting Development Issues

### ModuleNotFoundError

```bash
# Ensure package is installed
uv pip install -e .

# Check PYTHONPATH for MCP Inspector
PYTHONPATH=. mcp dev {{ cookiecutter.__project_slug }}/server/app.py
```

### Import Errors

- Verify all `__init__.py` files exist
- Use absolute imports: `from {{ cookiecutter.__project_slug }}.tools import my_tool`
- Check virtual environment is activated

### Transport Issues

- **STDIO**: Check for stdout pollution (use stderr for debugging)
- **SSE/HTTP**: Verify port availability and firewall settings
- **Docker**: Use `python scripts/docker.py status` and `python scripts/docker.py logs` to diagnose container issues
- **General**: Check logs for detailed error messages

### Decorator Issues

- Ensure decorators are applied in correct order
- Check correlation ID propagation
- Verify async/await compatibility

### Testing Issues

```bash
# Clean pytest cache
pytest --cache-clear

# Run tests in isolation
pytest --forked

# Check test dependencies
uv pip list | grep pytest
```

## Advanced Features

### Custom Log Destinations

Create new log destination:

```python
# log_system/destinations/my_destination.py
from .base import BaseDestination

class MyDestination(BaseDestination):
    async def log(self, entry: LogEntry) -> None:
        # Implement custom logging logic
        pass

    async def close(self) -> None:
        # Cleanup resources
        pass
```

Register in factory:

```python
# log_system/destinations/factory.py
def create_destination(dest_type: str, settings: Dict) -> BaseDestination:
    if dest_type == "my_destination":
        return MyDestination(settings)
    # ... existing destinations
```

### Custom Decorators

Create new decorator:

```python
# decorators/my_decorator.py
def my_decorator(func):
    """Custom decorator for specific functionality."""
    async def wrapper(*args, **kwargs):
        # Pre-processing
        result = await func(*args, **kwargs)
        # Post-processing
        return result
    return wrapper
```

Apply in server:

```python
# Apply custom decorator in decorator chain
decorated_func = my_decorator(exception_handler(tool_logger(func)))
```

### Configuration Extensions

Extend configuration:

```python
# config.py
class ServerConfig:
    my_setting: str = "default_value"
    my_number: int = 42
```

Use in tools:

```python
async def my_tool(ctx: Context = None) -> str:
    config = get_config()
    return f"Setting: {config.my_setting}"
```

This development guide should help you understand and extend the MCP Server Project effectively. Remember to run tests and follow coding standards when contributing.
