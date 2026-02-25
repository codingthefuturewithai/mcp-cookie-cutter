#!/usr/bin/env python
"""Post-generation hook for MCP Server Cookie Cutter.

This hook automatically:
1. Creates a virtual environment
2. Installs dependencies with uv
3. Shows helpful next steps
"""

import sys
import os
import platform
import subprocess
from pathlib import Path
import yaml

# Try to import platformdirs, but handle if it's not available
try:
    import platformdirs

    HAS_PLATFORMDIRS = True
except ImportError:
    HAS_PLATFORMDIRS = False


def run_command(cmd, description, check=True):
    """Run a command and handle errors gracefully."""
    print(f"   {description}...")
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=False,  # Don't raise exception on non-zero exit code
        )
        if result.returncode == 0:
            print(f"   {description} completed")
            return True
        else:
            print(
                f"   WARNING: {description} failed with exit code {result.returncode}"
            )
            # Show stderr if available
            if result.stderr:
                print(f"\n   Error details:")
                # Indent each line of the error for readability
                for line in result.stderr.strip().split("\n"):
                    print(f"      {line}")
            # Also show stdout if it contains error info (some tools output errors to stdout)
            elif result.stdout and "error" in result.stdout.lower():
                print(f"\n   Output:")
                for line in result.stdout.strip().split("\n"):
                    print(f"      {line}")
            return False
    except FileNotFoundError:
        print(f"   WARNING: Command not found: {cmd[0]}")
        return False
    except Exception as e:
        print(f"   WARNING: {description} failed with unexpected error: {e}")
        return False


def check_uv_installed():
    """Check if uv is installed."""
    result = run_command(["uv", "--version"], "Checking for uv", check=False)
    if not result:
        print("\n   uv is not installed. Installing uv...")
        # Try to install uv
        if platform.system() == "Windows":
            install_cmd = [
                "powershell",
                "-Command",
                "irm https://astral.sh/uv/install.ps1 | iex",
            ]
        else:
            install_cmd = [
                "sh",
                "-c",
                "curl -LsSf https://astral.sh/uv/install.sh | sh",
            ]

        if run_command(install_cmd, "Installing uv", check=False):
            print("   uv installed successfully")
            return True
        else:
            print("   WARNING: Could not install uv automatically")
            print("   Please install uv manually: https://github.com/astral-sh/uv")
            return False
    return True


def create_virtual_environment():
    """Create a virtual environment using uv."""
    print("\nSetting up Python environment...")

    # Check if .venv already exists
    venv_path = Path.cwd() / ".venv"
    if venv_path.exists():
        print("   Virtual environment already exists")
        return True

    # Create virtual environment with uv
    return run_command(["uv", "venv", ".venv"], "Creating virtual environment")


def install_dependencies():
    """Install project dependencies using uv."""
    print("\nInstalling dependencies...")

    # Install dependencies with uv sync (installs from pyproject.toml)
    success = run_command(
        ["uv", "sync", "--all-extras"],
        "Installing dependencies with uv sync (including dev, ui, and monitoring extras)",
    )

    # Note: --all-extras already includes ui, dev, and monitoring dependencies
    return success


def create_default_config():
    """Create a default config.yaml file for the MCP server.

    Creates the configuration in the platform-specific directory
    following XDG/Windows/macOS standards.
    """
    print("\nCreating default configuration...")

    try:
        app_name = "{{ cookiecutter.__project_slug }}"

        # Get platform-specific directories
        if HAS_PLATFORMDIRS:
            # Use platformdirs if available (likely on Mac/Linux with system Python)
            config_dir = Path(platformdirs.user_config_dir(app_name))
            data_dir = Path(platformdirs.user_data_dir(app_name))
            log_dir = Path(platformdirs.user_log_dir(app_name))
        else:
            # Fallback to manual platform detection (for Windows in cookiecutter environment)
            home = Path.home()
            if platform.system() == "Windows":
                # Windows: Use %APPDATA% for config and data, %LOCALAPPDATA% for logs
                appdata = Path(os.environ.get("APPDATA", home / "AppData" / "Roaming"))
                localappdata = Path(
                    os.environ.get("LOCALAPPDATA", home / "AppData" / "Local")
                )
                config_dir = appdata / app_name
                data_dir = appdata / app_name
                log_dir = localappdata / app_name / "Logs"
            elif platform.system() == "Darwin":
                # macOS
                config_dir = home / "Library" / "Application Support" / app_name
                data_dir = home / "Library" / "Application Support" / app_name
                log_dir = home / "Library" / "Logs" / app_name
            else:
                # Linux/Unix
                config_dir = home / ".config" / app_name
                data_dir = home / ".local" / "share" / app_name
                log_dir = home / ".local" / "state" / app_name

        # Create directory if it doesn't exist
        config_dir.mkdir(parents=True, exist_ok=True)

        config_file = config_dir / "config.yaml"

        # Check if config already exists
        if config_file.exists():
            print(f"   Configuration already exists at: {config_file}")
            return True

        # Default configuration matching UI's expected structure
        default_config = {
            "server": {
                "name": "{{ cookiecutter.project_name }}",
                "description": "{{ cookiecutter.description }}",
                "port": int("{{ cookiecutter.server_port }}"),
                "log_level": "INFO",
                "default_transport": "stdio",
                "default_host": "127.0.0.1",
            },
            "logging": {
                "level": "INFO",
                "retention_days": 30,
                "database_name": "unified_logs.db",
                "destinations": [{"type": "sqlite", "enabled": True, "settings": {}}],
            },
        }

        # Write config file
        with open(config_file, "w", encoding="utf-8") as f:
            yaml.dump(default_config, f, default_flow_style=False, sort_keys=False)

        print(f"   Created default configuration at:")
        print(f"      {config_file}")

        # Create data and log directories (already defined above)
        data_dir.mkdir(parents=True, exist_ok=True)
        log_dir.mkdir(parents=True, exist_ok=True)

        print(f"   Created data directory at:")
        print(f"      {data_dir}")
        print(f"   Created log directory at:")
        print(f"      {log_dir}")

        return True

    except Exception as e:
        print(f"   WARNING: Could not create configuration: {e}")
        print(f"   You can create it manually later by running the server")
        # Don't fail the entire generation for this
        return False


def show_next_steps():
    """Show helpful next steps to the user."""
    project_name = "{{ cookiecutter.project_name }}"
    project_slug = "{{ cookiecutter.__project_slug }}"

    print("\n" + "=" * 60)
    print(f"{project_name} created successfully!")
    print("=" * 60)

    print("\nNEXT STEPS - Follow these in order:")

    print(f"\n[1] Enter your project and activate the environment:")
    print(f"    # Open a new terminal window, then:")
    print(f"    cd {project_slug}")

    # Platform-specific activation command
    if platform.system() == "Windows":
        print(f"    # For PowerShell:")
        print(f"    .\\.venv\\Scripts\\Activate.ps1")
        print(f"    # For Command Prompt (cmd):")
        print(f"    .venv\\Scripts\\activate.bat")
    else:
        print(f"    source .venv/bin/activate       # Mac/Linux")

    print(f"\n[2] Verify your installation:")
    print(f'    {project_slug}-client "Hello World"')
    print(f"    ")
    print(f'    Expected output: "Echo: Hello World"')

    print(f"\n[3] Open the Admin UI for documentation and monitoring:")
    print(f"    # In a NEW terminal window:")
    print(f"    cd {project_slug}")
    if platform.system() == "Windows":
        print(f"    # For PowerShell:")
        print(f"    .\\.venv\\Scripts\\Activate.ps1")
        print(f"    # For Command Prompt (cmd):")
        print(f"    .venv\\Scripts\\activate.bat")
    else:
        print(f"    source .venv/bin/activate")
    print(f"    streamlit run {project_slug}/ui/app.py")
    print(f"    ")
    print(f"    -> Browser opens at http://localhost:8501")
    print(f'    -> Click "Documentation" in sidebar for comprehensive guides')
    print(f"    -> View logs and configure your server")

    print(f"\n[4] Test with MCP Inspector (optional):")
    print(f"    # In a NEW terminal window:")
    print(f"    cd {project_slug}")
    if platform.system() == "Windows":
        print(f"    # For PowerShell:")
        print(f"    .\\.venv\\Scripts\\Activate.ps1")
        print(f"    # For Command Prompt (cmd):")
        print(f"    .venv\\Scripts\\activate.bat")
    else:
        print(f"    source .venv/bin/activate")
    print(f"    fastmcp dev inspector {project_slug}/server/app.py")

    print("\n" + "=" * 60)

    print("\nDOCUMENTATION")
    print("\nAll documentation is available in the Admin UI:")
    print("  - Getting started guides")
    print("  - Adding new tools")
    print("  - Testing your tools")
    print("  - Different transport modes (SSE, HTTP)")
    print("  - Correlation ID tracking")
    print("  - And much more...")

    print("\nFor Claude Code users: Type /claude getting-started")

    print("\n" + "=" * 60)


def main():
    """Main entry point for the post-generation hook."""
    print("\nRunning post-generation setup...")

    # Check and install uv if needed
    if not check_uv_installed():
        print("\nSetup incomplete: uv is required")
        print("   Please install uv and run 'uv sync' manually")
        return

    # Create virtual environment
    if not create_virtual_environment():
        print("\nSetup incomplete: Could not create virtual environment")
        print("   Please create a virtual environment manually")
        return

    # Install dependencies
    if not install_dependencies():
        print("\nSetup incomplete: Could not install all dependencies")
        print("   Please run 'uv sync' manually")

    # Create default configuration
    create_default_config()

    # Show next steps
    show_next_steps()

    print("\nPost-generation setup completed!")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\nPost-generation hook failed: {e}")
        print("   You may need to set up the environment manually")

    # Always exit successfully to not break cookiecutter
    sys.exit(0)
