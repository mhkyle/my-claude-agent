# Gotchas

- `ANTHROPIC_BASE_URL` must be the root URL (e.g. `http://127.0.0.1:11434`).
  The CLI appends `/v1/messages`; do **not** include `/v1`.
- The SDK loads `.claude/` from `<cwd>/.claude/` with no parent-directory
  fallback, so the agent's `cwd` must be the repo root for this harness to load.
  `CWD=.` in `.env` (or the process cwd) ensures that.
- `setting_sources` must include `"project"` to load `CLAUDE.md`, agents, and
  skills. We use `["project", "local"]` to load the repo harness plus personal
  `settings.local.json`, while excluding `~/.claude`.
- `system_prompt=None` maps to an **empty** prompt (`--system-prompt ""`), not
  the default. Use `{"type": "preset", "preset": "claude_code"}` to keep Claude
  Code's default prompt.
- Subagents are invoked with the **`Agent`** tool (renamed from `Task` in Claude
  Code v2.1.63). The main session needs `Agent` in `allowed_tools`.
- Docker: the harness is not baked into the image; it arrives via the
  `-v "$PWD:/work"` mount, and `CWD=/work` points the agent at it.
- The SDK wheel bundles the `claude` binary, so no Node/npm is needed in the
  image.
- MCP: `.mcp.json` is empty by default. To enable a server, copy an entry from
  `.mcp.json.example` into `.mcp.json`, then add its tools (e.g.
  `mcp__filesystem__*`) to `allowed_tools` in `agent.py` or to
  `permissions.allow` in `.claude/settings.json`.
