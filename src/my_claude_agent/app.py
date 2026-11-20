"""FastAPI HTTP layer: stateless /chat plus multi-turn sessions."""

import asyncio
import uuid

from claude_agent_sdk import ClaudeSDKClient
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from .agent import build_options, format_message, stream

app = FastAPI(title="my-claude-agent")

sessions: dict[str, ClaudeSDKClient] = {}
locks: dict[str, asyncio.Lock] = {}


class ChatRequest(BaseModel):
    prompt: str


class SessionCreate(BaseModel):
    cwd: str | None = None


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/chat")
async def chat(req: ChatRequest) -> StreamingResponse:
    """One-shot request; a fresh agent process handles each call."""
    return StreamingResponse(stream(req.prompt), media_type="text/plain")


@app.post("/sessions")
async def create_session(req: SessionCreate | None = None) -> dict[str, str]:
    sid = uuid.uuid4().hex
    client = ClaudeSDKClient(options=build_options(req.cwd if req else None))
    await client.connect()
    sessions[sid] = client
    locks[sid] = asyncio.Lock()
    return {"session_id": sid}


@app.post("/sessions/{sid}/messages")
async def send_message(sid: str, req: ChatRequest) -> StreamingResponse:
    client = sessions.get(sid)
    if client is None:
        raise HTTPException(status_code=404, detail="no such session")

    async def gen():
        async with locks[sid]:  # one turn at a time per session
            await client.query(req.prompt)
            async for message in client.receive_response():
                chunk = format_message(message)
                if chunk:
                    yield chunk + "\n"

    return StreamingResponse(gen(), media_type="text/plain")


@app.delete("/sessions/{sid}")
async def close_session(sid: str) -> dict[str, bool]:
    client = sessions.pop(sid, None)
    if client is not None:
        await client.disconnect()
    locks.pop(sid, None)
    return {"ok": True}
