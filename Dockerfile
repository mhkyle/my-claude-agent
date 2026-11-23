FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

# git + ripgrep + bash are used by the Claude Code CLI's tools
RUN apt-get update && apt-get install -y --no-install-recommends \
        git \
        ripgrep \
        bash \
        ca-certificates \
        curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PYTHON=3.12 \
    PYTHONUNBUFFERED=1

# Install dependencies first so this layer is cached independently of source changes.
# The lockfile carries the Linux wheels, which bundle the platform's `claude` binary.
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev --no-install-project

COPY README.md ./
COPY src ./src
RUN uv sync --frozen --no-dev

# The harness (.claude/, CLAUDE.md, .mcp.json) is supplied by the host mount at
# /work (see README); CWD=/work points the agent at it. Nothing is baked in.
ENV PATH="/app/.venv/bin:$PATH" \
    HOME=/data \
    CLAUDE_CONFIG_DIR=/data/claude \
    CWD=/work \
    MODEL=qwen3.8:27b \
    ANTHROPIC_AUTH_TOKEN=ollama \
    ANTHROPIC_API_KEY="" \
    ANTHROPIC_BASE_URL=http://host.docker.internal:11434

RUN mkdir -p /data/claude /work

EXPOSE 8080

CMD ["uvicorn", "my_claude_agent.app:app", "--host", "0.0.0.0", "--port", "8080"]
