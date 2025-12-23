# MCP Server Cookie Cutter Template

A cookie cutter template for creating new MCP (Model Context Protocol) servers. This template generates a fully functional MCP server with multi-transport support (stdio, SSE, and streamable HTTP), advanced logging, automatic decorators, and a web-based management UI.

## Features

- **Multi-Transport Support**: stdio, SSE, and streamable HTTP in a single implementation
- **Automatic Decorators**: Exception handling, logging, type conversion, and parallelization
- **Unified Logging System**: SQLite-based logging with correlation IDs and extensible destinations
- **Web Management UI**: Streamlit-based interface for configuration, logs, and documentation
- **Example Tools**: Ready-to-use example tools with best practices
- **Full MCP Inspector Compatibility**: Easy testing and debugging
- **Proper Absolute Imports**: Clean package structure throughout
- **DevFlow Integration**: Built-in JIRA workflow commands (plan-work, implement, security-review, complete)
- **Comprehensive Documentation**: Templates for README, development guide, and setup prompts

## Prerequisites

1. Python 3.11 or higher

   ```bash
   python --version  # Should be 3.11 or higher
   ```

2. uv (Fast Python package installer)

   ```bash
   # Install uv if you don't have it
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

3. Cookie Cutter
   ```bash
   uv pip install cookiecutter
   ```

## Creating a New MCP Server

You can create a new MCP server either directly from GitHub or from a local copy of this template.

### Option 1: Directly from GitHub

```bash
cookiecutter gh:codingthefuturewithai/mcp-cookie-cutter
```

### Option 2: From Local Copy

1. Clone this template:

   ```bash
   git clone https://github.com/codingthefuturewithai/mcp-cookie-cutter
   ```

2. Create a project using the local template:
   ```bash
   cookiecutter path/to/mcp-cookie-cutter
   ```

### Template Configuration

You'll be asked for:

- `project_name`: Human-readable name (e.g., "My MCP Server")
- `__project_slug`: Python package name (auto-generated from project_name, e.g., "my_mcp_server")
- `description`: Short description of your project
- `author_name`: Your name
- `email`: Your email address
- `server_port`: Port for SSE and HTTP transports (default: 3001)

## Generated Project Structure

```
my_mcp_server/              # Your project directory
├── .claude/                # Claude Code integration
│   ├── agents/            # Security scanner agent
│   └── commands/          # DevFlow workflow commands
│       └── devflow/       # JIRA-integrated development workflow
├── my_mcp_server/          # Python package directory
│   ├── __init__.py
│   ├── __main__.py
│   ├── client/             # Client implementations
│   │   ├── __init__.py
│   │   └── app.py         # Test client for development
│   ├── server/            # Server implementation
│   │   ├── __init__.py
│   │   └── app.py        # Multi-transport MCP server (stdio, SSE, HTTP)
│   ├── tools/             # Tool implementations
│   │   ├── __init__.py
│   │   └── example_tools.py  # Example tools with decorators
│   ├── decorators/        # Automatic tool decorators
│   │   ├── exception_handler.py
│   │   ├── tool_logger.py
│   │   ├── type_converter.py
│   │   └── parallelize.py
│   ├── log_system/        # Unified logging system
│   │   ├── correlation.py     # Correlation ID tracking
│   │   ├── unified_logger.py  # Main logging interface
│   │   └── destinations/      # Log destinations (SQLite, etc.)
│   ├── ui/                # Streamlit management UI
│   │   ├── app.py
│   │   ├── lib/          # UI components and utilities
│   │   └── pages/        # UI pages (Home, Config, Logs, Docs)
│   ├── config.py          # Server configuration
│   └── logging_config.py  # Logging setup
├── tests/                 # Test suite
│   ├── unit/             # Unit tests
│   └── integration/      # Integration tests
├── pyproject.toml         # Project configuration and dependencies
├── README.md             # Project documentation template
├── DEVELOPMENT.md        # Development guide
├── DEVELOPER_GUIDE.md    # Developer reference
└── SETUP_PROMPT.md       # AI-assisted setup guide
```

## Next Steps

Once your project is generated:

1. **Review Documentation Templates**
   - Customize `README.md` for your project
   - Review `DEVELOPMENT.md` for development workflow
   - Check `DEVELOPER_GUIDE.md` for architectural details
   - Use `SETUP_PROMPT.md` for AI-assisted setup

2. **Set Up Development Environment**
   - Install dependencies: `uv pip install -e .`
   - Run tests: `pytest`
   - Start the server: `python -m your_project_name --transport stdio`

3. **Explore Transports**
   - **STDIO**: `python -m your_project_name --transport stdio`
   - **SSE**: `python -m your_project_name --transport sse --port 3001`
   - **Streamable HTTP**: `python -m your_project_name --transport streamable-http --port 3001`

4. **Test with MCP Inspector**
   - Install: `npm install -g @modelcontextprotocol/inspector`
   - Run: `mcp dev your_project_name/server/app.py`

5. **Access Management UI**
   - Start UI: `streamlit run your_project_name/ui/app.py`
   - View logs, configure server, browse documentation

6. **Add Your Own Tools**
   - Add functions to `tools/example_tools.py`
   - Decorators are applied automatically
   - Register in `example_tools` or `parallel_example_tools` lists

7. **Use DevFlow Workflow** (Optional)
   - Connect to JIRA
   - Use `/devflow:plan-work ISSUE-KEY` to plan
   - Use `/devflow:implement ISSUE-KEY` to implement
   - Use `/devflow:security-review ISSUE-KEY` to scan
   - Use `/devflow:complete ISSUE-KEY` to create PR

## License

This template is licensed under the MIT License - see the LICENSE file for details.
