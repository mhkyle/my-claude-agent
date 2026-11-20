FROM python:3.12-slim
RUN apt-get update && apt-get install -y --no-install-recommends git ripgrep \
 && rm -rf /var/lib/apt/lists/*
WORKDIR /app
RUN pip install --no-cache-dir claude-agent-sdk fastapi "uvicorn[standard]"
COPY app.py .
ENV CLAUDE_CONFIG_DIR=/data/claude
RUN mkdir -p /data/claude
EXPOSE 8080
CMD ["uvicorn","app:app","--host","0.0.0.0","--port","8080"]
