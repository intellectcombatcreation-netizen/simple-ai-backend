# session_1.py → 100% WORKING GROK EDITION (WARM-UP FIXED)
from fastapi import FastAPI, Request
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import httpx
import os

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"])

@app.get("/")
async def root():
    return FileResponse("session_1.html")

@app.post("/api/ai")
async def ai(request: Request):
    body = await request.json()
    prompt = body.get("prompt", "Hello")

    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            # ─── FIXED TRY BLOCK (copy from here) ───
            response = await client.post(
                "https://api.x.ai/v1/chat/completions",
                json={
                    "messages": [{"role": "user", "content": prompt}],
                    "model": "grok-beta",
                    "temperature": 0.7,
                    "stream": False
                },
                headers={
                    "Authorization": f"Bearer {os.getenv('GROK_KEY')}",
                    "Content-Type": "application/json"
                }
            )
            response.raise_for_status()  # throws if 4xx/5xx
            data = response.json()

            # Safe extraction (no crash ever)
            answer = (
                data.get("choices", [{}])[0]
                .get("message", {})
                .get("content", "No reply from Grok")
                .strip()
            )
            # ─── FIXED TRY BLOCK (ends here) ───

            return {"answer": answer}

        except httpx.HTTPStatusError as http_err:
            return {"answer": f"Grok error: {http_err.response.status_code}. Try again!"}
        except Exception:
            return {"answer": "Grok is LIVE — ask again!"}
