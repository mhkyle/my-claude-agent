#!/usr/bin/env bash
# PostToolUse hook: run available checks after file edits.
#
# Intentionally non-blocking (exit 0) until a test/lint setup exists.
# TODO: add `uv run pytest` / `uv run ruff check` once configured, and make
#       failures exit non-zero so the agent can react to them.
set -euo pipefail

root="${CLAUDE_PROJECT_DIR:-$(git rev-parse --show-toplevel 2>/dev/null || pwd)}"
cd "$root" 2>/dev/null || exit 0

if command -v ruff >/dev/null 2>&1; then
  ruff check . || true
fi

# No test runner configured yet — no-op.
exit 0
