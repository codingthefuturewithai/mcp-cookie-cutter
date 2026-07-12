"""Example MCP prompts for {{ cookiecutter.project_name }}

Prompts are reusable, user-controlled message templates. Hosts typically
surface them as slash commands or quick actions; the user picks one and
the client fills in the arguments.

Two patterns are demonstrated:
1. Simple prompt        - returns a single string
2. Multi-message prompt - returns a structured conversation

Add your own prompts here and they will be registered by
register_prompts() in server/app.py.
"""

from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp.prompts import base


def register_prompts(mcp_server: FastMCP) -> None:
    """Register all example prompts with the MCP server."""

    @mcp_server.prompt(title="Review Code")
    def review_code(code: str) -> str:
        """Ask the model to review a piece of code."""
        return (
            "Please review the following code for correctness, clarity, "
            f"and potential bugs:\n\n{code}"
        )

    @mcp_server.prompt(title="Debug an Error")
    def debug_error(error: str) -> list[base.Message]:
        """Start a structured debugging conversation for an error message."""
        return [
            base.UserMessage("I'm running into this error:"),
            base.UserMessage(error),
            base.AssistantMessage(
                "I'll help you debug that. What have you tried so far, "
                "and when did the error first appear?"
            ),
        ]
