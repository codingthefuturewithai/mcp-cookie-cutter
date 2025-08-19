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


def run_command(cmd, description, check=True):
    """Run a command and handle errors gracefully."""
    print(f"   {description}...")
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=check
        )
        if result.returncode == 0:
            print(f"   ✅ {description} completed")
            return True
        else:
            print(f"   ⚠️  {description} failed")
            if result.stderr:
                print(f"      Error: {result.stderr}")
            return False
    except FileNotFoundError:
        print(f"   ⚠️  Command not found: {cmd[0]}")
        return False
    except Exception as e:
        print(f"   ⚠️  {description} failed: {e}")
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
        # Also install the project in editable mode
        run_command(
            ["uv", "pip", "install", "-e", "."],
            "Installing project in editable mode"
        )
    
    return success


def show_next_steps():
    """Show helpful next steps to the user."""
    project_name = "{{ cookiecutter.project_name }}"
    project_slug = "{{ cookiecutter.project_slug }}"
    
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
    
    print(f"\n📚 Features included:")
    print(f"   ✅ 10 example tools (8 regular + 2 parallel)")
    print(f"   ✅ 4 decorators (exception_handler, tool_logger, type_converter, parallelize)")
    print(f"   ✅ 3 transports (stdio, sse, streamable-http)")
    print(f"   ✅ Correlation ID tracking")
    print(f"   ✅ Unified logging with SQLite")
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