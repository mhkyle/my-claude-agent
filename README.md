# my-claude-agent

A small wrapper around the Claude Agent SDK that runs against a local Ollama
model, with both a CLI and an HTTP API.

## Requirements

- Python 3.12+ (managed by `uv`; the container image uses 3.12)
- Ollama serving a model, e.g. `qwen3.8:27b`
- Docker (optional, for the container image)

## Configuration

Settings are read from `.env`:

```dotenv
ANTHROPIC_BASE_URL=http://127.0.0.1:11434
ANTHROPIC_AUTH_TOKEN=ollama
ANTHROPIC_API_KEY=
MODEL=qwen3.8:27b
CWD=src/my_claude_agent
```

> `ANTHROPIC_BASE_URL` must be the root URL — the CLI appends `/v1/messages`
> itself. Do not add `/v1`.

## Harness (`.claude/`)

Agent behaviour is driven by the repo-root `.claude/` directory, plus a small
root `CLAUDE.md` that imports the detailed knowledge:

| Path | Purpose |
| --- | --- |
| `CLAUDE.md` | Role + project knowledge, loaded every session (imports `.claude/knowledge/`). |
| `.claude/knowledge/` | Detailed project overview and gotchas. |
| `.claude/agents/` | Subagents: `reviewer` (read-only) and `debugger`. |
| `.claude/skills/` | Auto-invoked skills: `sre` and `compute`. |
| `.claude/settings.json` | Permissions and a `PostToolUse` check hook. |
| `.claude/settings.local.json` | Personal overrides (gitignored). |
| `.claude/hooks/run-tests.sh` | Non-blocking post-edit check. |
| `.mcp.json` / `.mcp.json.example` | MCP config (empty by default; see the example). |

How it is wired in `agent.build_options()`: `cwd` defaults to the repo root,
`setting_sources=["project", "local"]` loads this harness (excluding
`~/.claude`), `system_prompt` uses the `claude_code` preset so `CLAUDE.md`
augments it, `skills="all"` enables the skills, and `Agent` is allowed so the
subagents can be invoked.

> The SDK loads `.claude/` from `<cwd>/.claude/`, so run the agent from the repo
> root (keep `CWD=.` in `.env`).

## CLI

```bash
uv run main.py "review utils.py"
# or the console script
uv run my-claude-agent "review utils.py"
```

## HTTP API

```bash
uv run uvicorn my_claude_agent.app:app --port 8080
```

| Method | Path | Description |
| --- | --- | --- |
| `POST` | `/chat` | One-shot request. Body: `{"prompt": "..."}`. Streams the reply. |
| `POST` | `/sessions` | Create a multi-turn session. Returns `{"session_id": "..."}`. |
| `POST` | `/sessions/{sid}/messages` | Send a turn. Body: `{"prompt": "..."}`. Streams the reply. |
| `DELETE` | `/sessions/{sid}` | Close and remove a session. |
| `GET` | `/health` | Liveness check. |

```bash
curl -N -X POST localhost:8080/chat \
  -H 'content-type: application/json' \
  -d '{"prompt":"review utils.py"}'
```

## Docker

The container reaches Ollama on the host at `host.docker.internal:11434`.
Docker Desktop (macOS/Windows) proxies host loopback, so a default Ollama
install bound to `127.0.0.1:11434` works as-is.

On Linux, either pass `--add-host=host.docker.internal:host-gateway` and bind
Ollama to `0.0.0.0:11434`, or run the container with `--network host` and set
`ANTHROPIC_BASE_URL=http://127.0.0.1:11434`.

Build and run, mounting a workspace at `/work`:

```bash
docker build -t my-claude-agent .
docker run --rm -p 8080:8080 -v "$PWD:/work" my-claude-agent
curl -N -X POST localhost:8080/chat \
  -H 'content-type: application/json' -d '{"prompt":"review utils.py"}'
```

The SDK wheel bundles the platform's `claude` binary, so no Node/npm install is
needed inside the image. Override `ANTHROPIC_BASE_URL` at runtime with
`-e ANTHROPIC_BASE_URL=...` if needed.
