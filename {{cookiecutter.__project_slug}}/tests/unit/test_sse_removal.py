"""Tests validating SSE transport has been removed from the generated project.

These tests ensure that the deprecated SSE transport is no longer available
in the generated MCP server, per issue #4. Only stdio and streamable-http
transports should be supported.

Acceptance criteria validated:
- CLI rejects --transport sse
- No main_sse entry point function exists
- No run_sse_async calls in server source code
- No *-server-sse entry point in pyproject.toml
- Only ["stdio", "streamable-http"] in CLI transport choices
"""

import ast
import re
from pathlib import Path

import pytest


# Path to the server app module source (template source, not rendered)
SERVER_APP_PATH = Path(__file__).parent.parent.parent / "{{ cookiecutter.__project_slug }}" / "server" / "app.py"
INIT_PATH = Path(__file__).parent.parent.parent / "{{ cookiecutter.__project_slug }}" / "__init__.py"
PYPROJECT_PATH = Path(__file__).parent.parent.parent / "pyproject.toml"


class TestSSETransportRemoval:
    """Validate that SSE transport has been fully removed."""

    def test_no_main_sse_function_in_server_app(self):
        """The main_sse() entry point function must not exist in server/app.py."""
        source = SERVER_APP_PATH.read_text()
        # Parse the AST to find function definitions
        # Since this is a template file with Jinja2, we search the raw text
        assert "def main_sse" not in source, (
            "main_sse() function still exists in server/app.py — it should be removed"
        )

    def test_no_sse_in_cli_transport_choices(self):
        """The --transport CLI option must not include 'sse' as a choice."""
        source = SERVER_APP_PATH.read_text()
        # Find the click.Choice line for transport
        choice_match = re.search(r'click\.Choice\(\[([^\]]+)\]\)', source)
        assert choice_match is not None, "Could not find click.Choice for transport in server/app.py"
        choices_str = choice_match.group(1)
        # Extract individual choices
        choices = [c.strip().strip('"').strip("'") for c in choices_str.split(",")]
        assert "sse" not in choices, (
            f"'sse' still in transport choices: {choices} — should only be ['stdio', 'streamable-http']"
        )
        assert choices == ["stdio", "streamable-http"], (
            f"Transport choices should be exactly ['stdio', 'streamable-http'], got {choices}"
        )

    def test_no_run_sse_async_in_server_app(self):
        """No calls to run_sse_async() should exist in server/app.py."""
        source = SERVER_APP_PATH.read_text()
        assert "run_sse_async" not in source, (
            "run_sse_async() call still exists in server/app.py — SSE code path should be removed"
        )

    def test_no_run_sse_async_in_init(self):
        """No calls to run_sse_async() should exist in __init__.py."""
        source = INIT_PATH.read_text()
        assert "run_sse_async" not in source, (
            "run_sse_async() call still exists in __init__.py — should use run_streamable_http_async()"
        )

    def test_no_sse_entry_point_in_pyproject(self):
        """The *-server-sse entry point must not exist in pyproject.toml."""
        source = PYPROJECT_PATH.read_text()
        assert "server-sse" not in source, (
            "server-sse entry point still exists in pyproject.toml — it should be removed"
        )
        assert "main_sse" not in source, (
            "main_sse reference still exists in pyproject.toml — it should be removed"
        )

    def test_no_sse_transport_elif_block(self):
        """The elif transport == 'sse' block must not exist in server/app.py."""
        source = SERVER_APP_PATH.read_text()
        assert 'transport == "sse"' not in source, (
            "SSE transport branch still exists in server/app.py — the elif block should be removed"
        )
        assert "transport == 'sse'" not in source, (
            "SSE transport branch still exists in server/app.py — the elif block should be removed"
        )

    def test_server_app_help_text_no_sse(self):
        """CLI help text should not mention SSE."""
        source = SERVER_APP_PATH.read_text()
        # Check the help strings for port and transport options
        help_matches = re.findall(r'help="([^"]*)"', source)
        for help_text in help_matches:
            # Allow "SSE" only in a deprecation notice context, not as active documentation
            if "sse" in help_text.lower():
                assert False, (
                    f"CLI help text still mentions SSE: '{help_text}' — update to reference only Streamable HTTP"
                )

    def test_server_app_docstring_no_sse(self):
        """Module docstring should not reference SSE as a supported transport."""
        source = SERVER_APP_PATH.read_text()
        # Check the first docstring (module-level)
        docstring_match = re.search(r'^"""(.*?)"""', source, re.DOTALL)
        if docstring_match:
            docstring = docstring_match.group(1)
            # Skip the first line (project name) which may contain "SSE" as part
            # of a user-chosen project name like "Test SSE Removal"
            docstring_lines = docstring.strip().split("\n")
            description_lines = "\n".join(docstring_lines[1:]) if len(docstring_lines) > 1 else ""
            assert "SSE" not in description_lines, (
                f"Module docstring description still references SSE — update to mention only STDIO and Streamable HTTP"
            )
