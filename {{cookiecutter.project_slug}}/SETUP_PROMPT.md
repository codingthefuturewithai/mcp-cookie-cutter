# AI Assistant Setup Instructions for {{ cookiecutter.project_name }}

This document provides instructions for AI coding assistants to properly configure and use the {{ cookiecutter.project_name }} MCP server.

## Installation Method

**IMPORTANT**: Use ONLY the isolated `uv tool` installation method to avoid dependency conflicts.

### Step 1: Install the MCP Server

```bash
# Install as an isolated tool (REQUIRED - do not use pip or pipx)
uv tool install {{ cookiecutter.project_slug }}
```

### Step 2: Find the Binary Location

After installation, locate the installed binary path:

**macOS/Linux:**
```bash
which {{ cookiecutter.project_slug }}-server
# Example output: /Users/username/.local/bin/{{ cookiecutter.project_slug }}-server
```

**Windows:**
```bash
where {{ cookiecutter.project_slug }}-server
# Example output: C:\Users\username\.local\bin\{{ cookiecutter.project_slug }}-server.exe
```

### Step 3: Configure Your MCP Client

Use the ABSOLUTE PATH from Step 2 in your configuration:

**For Claude Desktop:**
Edit `~/Library/Application Support/Claude/claude_desktop_config.json` (macOS) or `%APPDATA%\Claude\claude_desktop_config.json` (Windows):

```json
{
  "mcpServers": {
    "{{ cookiecutter.project_slug }}": {
      "command": "/absolute/path/to/{{ cookiecutter.project_slug }}-server",
      "env": {
        "API_KEY": "your-api-key-here"
      }
    }
  }
}
```

**For Cline (VS Code):**
Add to `.vscode/settings.json`:

```json
{
  "cline.MCP.mcpServers": {
    "{{ cookiecutter.project_slug }}": {
      "command": "/absolute/path/to/{{ cookiecutter.project_slug }}-server",
      "env": {
        "API_KEY": "your-api-key-here"
      }
    }
  }
}
```

## Fallback: Using uvx (Less Reliable)

If `uv tool install` fails, you can use `uvx` as a fallback, but be aware of potential dependency conflicts:

```json
{
  "{{ cookiecutter.project_slug }}": {
    "command": "uvx",
    "args": ["{{ cookiecutter.project_slug }}-server"],
    "env": {
      "API_KEY": "your-api-key-here"
    }
  }
}
```

**WARNING**: The `uvx` method may fail if you have conflicting Python packages installed globally. Always prefer the `uv tool install` method.

## Verification

After configuration:

1. Restart your MCP client
2. Test the connection with: "Use the echo tool to test the connection"
3. If it fails, verify:
   - The binary path is correct and absolute
   - Required environment variables are set
   - No error messages in the MCP client logs

## Troubleshooting

### Binary Not Found
- Ensure `uv` is installed: `pip install uv`
- Verify installation: `uv tool list | grep {{ cookiecutter.project_slug }}`
- Check PATH: The binary location should be in your system PATH

### Dependency Conflicts
- Always use `uv tool install` instead of `pip install`
- If using `uvx` and encountering conflicts, switch to the isolated installation
- Check for conflicting packages: `uv pip list`

### Environment Variables
- Replace `your-api-key-here` with actual credentials
- Ensure no typos in variable names
- Some shells require escaping special characters in API keys