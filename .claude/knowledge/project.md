# Project: my-claude-agent

Wrapper around the Claude Agent SDK (Claude Code under the hood) pointing at a
local Ollama model. Python 3.12+, managed with `uv`.

## Layout

- `main.py` / `src/my_claude_agent/__init__.py` — CLI entry point.
- `src/my_claude_agent/agent.py` — `build_options()` plus streaming
  (`stream`, `main`).
- `src/my_claude_agent/app.py` — FastAPI: `/health`, `/chat`, `/sessions`.
- `src/my_claude_agent/utils.py` — small helpers.
- `.claude/` — this harness (knowledge, agents, skills, settings, hooks).
- `.mcp.json` — MCP server config (template; empty by default).

## Run

- CLI: `uv run main.py "review utils.py"` (or `uv run my-claude-agent "..."`).
- HTTP: `uv run uvicorn my_claude_agent.app:app --port 8080`.
- Docker: `docker build -t my-claude-agent .` then
  `docker run --rm -p 8080:8080 -v "$PWD:/work" my-claude-agent`.

## HTTP endpoints

- `POST /chat` — one-shot; body `{"prompt": "..."}`; streams text.
- `POST /sessions` — create a session; returns `{"session_id": "..."}`.
- `POST /sessions/{sid}/messages` — multi-turn; streams text.
- `DELETE /sessions/{sid}` — close and remove the session.
- `GET /health` — liveness check.

## Conventions

- Python 3.12+, type hints on public functions, `uv` for dependencies.
- Keep FastAPI handlers thin; agent logic stays in `agent.py`.
- <!-- TODO: add project-specific conventions (lint, tests, style). -->
