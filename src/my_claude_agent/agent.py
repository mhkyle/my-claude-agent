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


def build_options(cwd: str | None = None) -> ClaudeAgentOptions:
    """Build the Claude Agent SDK options from the environment.

    Behaviour is driven by the repo-root ``.claude/`` harness:

    - ``setting_sources`` loads the project + local ``.claude/`` config
      (``CLAUDE.md``, agents, skills, settings, hooks) and excludes ``~/.claude``.
    - ``system_prompt`` keeps Claude Code's default preset. Passing ``None``
      sends an *empty* system prompt (``--system-prompt ""``), so we set the
      preset explicitly and let ``CLAUDE.md`` augment it instead of replacing it.
    - ``skills="all"`` exposes ``.claude/skills/*`` (the SDK also adds the
      ``Skill`` tool for us).
    - ``Agent`` in ``allowed_tools`` lets the model invoke the subagents defined
      in ``.claude/agents/``.
    """
    return ClaudeAgentOptions(
        model=os.environ.get("MODEL", "qwen3.8:27b"),
        cwd=os.path.abspath(cwd or os.environ.get("CWD") or os.getcwd()),
        system_prompt={"type": "preset", "preset": "claude_code"},
        max_turns=int(os.environ.get("MAX_TURNS", "20")),
        allowed_tools=[
            "Read",
            "Glob",
            "Grep",
            "Edit",
            "Write",
            "Agent",  # invoke subagents defined in .claude/agents/
            # Add per-server MCP tools here, e.g. "mcp__filesystem__*",
            # once a server is enabled in .mcp.json.
        ],
        permission_mode="acceptEdits",
        setting_sources=["project", "local"],  # repo .claude/, not ~/.claude
        skills="all",
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
