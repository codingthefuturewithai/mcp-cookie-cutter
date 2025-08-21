#!/usr/bin/env python
"""Post-generation hook for MCP Server Cookie Cutter.

This hook automatically:
1. Creates a virtual environment
2. Installs dependencies with uv
3. Shows helpful next steps
"""

import sys
import platform
import subprocess
from pathlib import Path
import yaml
import platformdirs


def run_command(cmd, description, check=True):
    """Run a command and handle errors gracefully."""
    print(f"   {description}...")
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=False  # Don't raise exception on non-zero exit code
        )
        if result.returncode == 0:
            print(f"   ✅ {description} completed")
            return True
        else:
            print(f"   ⚠️  {description} failed with exit code {result.returncode}")
            # Show stderr if available
            if result.stderr:
                print(f"\n   Error details:")
                # Indent each line of the error for readability
                for line in result.stderr.strip().split('\n'):
                    print(f"      {line}")
            # Also show stdout if it contains error info (some tools output errors to stdout)
            elif result.stdout and 'error' in result.stdout.lower():
                print(f"\n   Output:")
                for line in result.stdout.strip().split('\n'):
                    print(f"      {line}")
            return False
    except FileNotFoundError:
        print(f"   ⚠️  Command not found: {cmd[0]}")
        return False
    except Exception as e:
        print(f"   ⚠️  {description} failed with unexpected error: {e}")
        return False


def check_uv_installed():
    """Check if uv is installed."""
    result = run_command(
        ["uv", "--version"],
        "Checking for uv",
        check=False
    )
    if not result:
        print("\n   📦 uv is not installed. Installing uv...")
        # Try to install uv
        if platform.system() == "Windows":
            install_cmd = ["powershell", "-Command", "irm https://astral.sh/uv/install.ps1 | iex"]
        else:
            install_cmd = ["sh", "-c", "curl -LsSf https://astral.sh/uv/install.sh | sh"]
        
        if run_command(install_cmd, "Installing uv", check=False):
            print("   ✅ uv installed successfully")
            return True
        else:
            print("   ⚠️  Could not install uv automatically")
            print("   Please install uv manually: https://github.com/astral-sh/uv")
            return False
    return True


def create_virtual_environment():
    """Create a virtual environment using uv."""
    print("\n🐍 Setting up Python environment...")
    
    # Check if .venv already exists
    venv_path = Path.cwd() / ".venv"
    if venv_path.exists():
        print("   ✅ Virtual environment already exists")
        return True
    
    # Create virtual environment with uv
    return run_command(
        ["uv", "venv", ".venv"],
        "Creating virtual environment"
    )


def install_dependencies():
    """Install project dependencies using uv."""
    print("\n📦 Installing dependencies...")
    
    # Install dependencies with uv sync (installs from pyproject.toml)
    success = run_command(
        ["uv", "sync"],
        "Installing dependencies with uv sync"
    )
    
    if success:
        # Install optional UI dependencies using uv sync with extras
        run_command(
            ["uv", "sync", "--extra", "ui"],
            "Installing optional UI dependencies (Streamlit)"
        )
    
    return success


def create_default_config():
    """Create a default config.yaml file for the MCP server.
    
    Creates the configuration in the platform-specific directory
    following XDG/Windows/macOS standards.
    """
    print("\n⚙️  Creating default configuration...")
    
    try:
        # Get platform-specific config directory
        app_name = "{{ cookiecutter.__project_slug }}"
        config_dir = Path(platformdirs.user_config_dir(app_name))
        
        # Create directory if it doesn't exist
        config_dir.mkdir(parents=True, exist_ok=True)
        
        config_file = config_dir / "config.yaml"
        
        # Check if config already exists
        if config_file.exists():
            print(f"   ℹ️  Configuration already exists at: {config_file}")
            return True
        
        # Get platform-specific data and log directories first
        data_dir = Path(platformdirs.user_data_dir(app_name))
        log_dir = Path(platformdirs.user_log_dir(app_name))
        
        # Default configuration matching UI's expected structure
        default_config = {
            "server": {
                "name": "{{ cookiecutter.project_name }}",
                "description": "{{ cookiecutter.description }}",
                "port": int("{{ cookiecutter.server_port }}"),
                "log_level": "INFO",
                "default_transport": "stdio",
                "default_host": "127.0.0.1"
            },
            "logging": {
                "level": "INFO",
                "retention_days": 30,
                "database_name": "unified_logs.db",
                "destinations": [
                    {
                        "type": "sqlite",
                        "enabled": True,
                        "settings": {}
                    }
                ]
            }
        }
        
        # Write config file
        with open(config_file, 'w', encoding='utf-8') as f:
            yaml.dump(default_config, f, default_flow_style=False, sort_keys=False)
        
        print(f"   ✅ Created default configuration at:")
        print(f"      {config_file}")
        
        # Create data and log directories (already defined above)
        data_dir.mkdir(parents=True, exist_ok=True)
        log_dir.mkdir(parents=True, exist_ok=True)
        
        print(f"   ✅ Created data directory at:")
        print(f"      {data_dir}")
        print(f"   ✅ Created log directory at:")
        print(f"      {log_dir}")
        
        return True
        
    except Exception as e:
        print(f"   ⚠️  Could not create configuration: {e}")
        print(f"   ℹ️  You can create it manually later by running the server")
        # Don't fail the entire generation for this
        return False


def show_next_steps():
    """Show helpful next steps to the user."""
    project_name = "{{ cookiecutter.project_name }}"
    project_slug = "{{ cookiecutter.__project_slug }}"
    
    print("\n" + "=" * 60)
    print(f"🎉 {project_name} created successfully!")
    print("=" * 60)
    
    print("\n📋 Quick Start:")
    print(f"   cd {project_slug}")
    
    # Platform-specific activation command
    if platform.system() == "Windows":
        activate_cmd = ".venv\\Scripts\\activate"
    else:
        activate_cmd = "source .venv/bin/activate"
    
    print(f"   {activate_cmd}")
    
    print(f"\n🚀 Run your server:")
    print(f"   # STDIO transport (default)")
    print(f"   {project_slug}-server")
    print(f"   ")
    print(f"   # SSE transport")
    print(f"   {project_slug}-server --transport sse --port 3001")
    print(f"   ")
    print(f"   # Streamable HTTP transport")
    print(f"   {project_slug}-server --transport streamable-http --port 3001")
    
    print(f"\n🧪 Test with MCP Inspector:")
    print(f"   PYTHONPATH=. mcp dev {project_slug}/server/app.py")
    
    print(f"\n🖥️ Run the Admin UI:")
    print(f"   streamlit run {project_slug}/ui/app.py")
    
    print(f"\n📚 Features included:")
    print(f"   ✅ 10 example tools (8 regular + 2 parallel)")
    print(f"   ✅ 4 decorators (exception_handler, tool_logger, type_converter, parallelize)")
    print(f"   ✅ 3 transports (stdio, sse, streamable-http)")
    print(f"   ✅ Correlation ID tracking")
    print(f"   ✅ Unified logging with SQLite")
    print(f"   ✅ Streamlit Admin UI")
    print(f"   ✅ Platform-aware configuration")
    
    print("\n" + "=" * 60)


def main():
    """Main entry point for the post-generation hook."""
    print("\n🔧 Running post-generation setup...")
    
    # Check and install uv if needed
    if not check_uv_installed():
        print("\n⚠️  Setup incomplete: uv is required")
        print("   Please install uv and run 'uv sync' manually")
        return
    
    # Create virtual environment
    if not create_virtual_environment():
        print("\n⚠️  Setup incomplete: Could not create virtual environment")
        print("   Please create a virtual environment manually")
        return
    
    # Install dependencies
    if not install_dependencies():
        print("\n⚠️  Setup incomplete: Could not install all dependencies")
        print("   Please run 'uv sync' manually")
    
    # Create default configuration
    create_default_config()
    
    # Show next steps
    show_next_steps()
    
    print("\n✅ Post-generation setup completed!")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n⚠️  Post-generation hook failed: {e}")
        print("   You may need to set up the environment manually")
    
    # Always exit successfully to not break cookiecutter
    sys.exit(0)