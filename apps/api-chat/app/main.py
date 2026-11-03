"""api-chat: forwards one message to OpenRouter. Exists to prove secret injection works in
preview and DevSpace. Routes live under /api/chat (see api-orders for why)."""
import os

import httpx
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

GIT_SHA = os.getenv("GIT_SHA", "dev")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")
OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "openai/gpt-4o-mini")

app = FastAPI(title="api-chat")


class ChatIn(BaseModel):
    message: str


@app.get("/api/chat/healthz")
async def healthz():
    return {"service": "api-chat", "sha": GIT_SHA, "model": OPENROUTER_MODEL, "keyConfigured": bool(OPENROUTER_API_KEY)}


@app.post("/api/chat")
async def chat(body: ChatIn):
    if not OPENROUTER_API_KEY:
        raise HTTPException(503, "OPENROUTER_API_KEY not configured")
    async with httpx.AsyncClient(timeout=60) as client:
        r = await client.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={"Authorization": f"Bearer {OPENROUTER_API_KEY}"},
            json={"model": OPENROUTER_MODEL, "max_tokens": 200,
                  "messages": [{"role": "user", "content": body.message}]},
        )
    if r.status_code != 200:
        raise HTTPException(502, f"openrouter {r.status_code}: {r.text[:200]}")
    return {"reply": r.json()["choices"][0]["message"]["content"]}
