"""Core agent logic: build SDK options and stream one request's response."""

import os
from collections.abc import AsyncIterator
from typing import Any

from dotenv import load_dotenv

from claude_agent_sdk import (
    AssistantMessage,
    ClaudeAgentOptions,
    ResultMessage,
    TextBlock,
    ToolUseBlock,
    query,
)

load_dotenv()

DEFAULT_SYSTEM_PROMPT = (
    "You are a helpful assistant with Cloud SRE expertise. You can help with "
    "code review, debugging, and fixing issues in Compute program code."
)


def build_options(cwd: str | None = None) -> ClaudeAgentOptions:
    """Build the Claude Agent SDK options from the environment."""
    return ClaudeAgentOptions(
        model=os.environ.get("MODEL", "qwen3.8:27b"),
        cwd=cwd or os.environ.get("CWD", "src/my_claude_agent"),
        system_prompt=os.environ.get("SYSTEM_PROMPT", DEFAULT_SYSTEM_PROMPT),
        max_turns=int(os.environ.get("MAX_TURNS", "20")),
        allowed_tools=["Read", "Glob", "Grep", "Edit", "Write"],
        permission_mode="acceptEdits",
        setting_sources=[],  # don't pull ~/.claude config in
        env={
            "ANTHROPIC_BASE_URL": os.environ.get(
                "ANTHROPIC_BASE_URL", "http://localhost:11434"
            ),
            "ANTHROPIC_AUTH_TOKEN": os.environ.get("ANTHROPIC_AUTH_TOKEN", "ollama"),
            "ANTHROPIC_API_KEY": os.environ.get("ANTHROPIC_API_KEY", ""),
            "CLAUDE_CODE_DISABLE_EXPERIMENTAL_BETAS": "1",
            "CLAUDE_CODE_DISABLE_AUTO_MEMORY": "1",
        },
    )


def format_message(message: Any) -> str | None:
    """Turn an SDK message into a printable chunk, or None to skip it."""
    if isinstance(message, AssistantMessage):
        parts: list[str] = []
        for block in message.content:
            if isinstance(block, TextBlock):
                parts.append(block.text)
            elif isinstance(block, ToolUseBlock):
                parts.append(f"[Tool: {block.name}]")
        return "\n".join(parts) if parts else None
    if isinstance(message, ResultMessage):
        return f"[Done: {message.subtype}]"
    return None


async def stream(prompt: str) -> AsyncIterator[str]:
    """Stream the agent's response to a single request."""
    async for message in query(prompt=prompt, options=build_options()):
        chunk = format_message(message)
        if chunk:
            yield chunk + "\n"


async def main(prompt: str) -> None:
    """CLI entry: print the agent's response for one request."""
    async for chunk in stream(prompt):
        print(chunk, end="", flush=True)
