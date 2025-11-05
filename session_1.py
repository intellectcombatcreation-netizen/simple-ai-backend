# session_1.py → 100% WORKING GROK EDITION
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
            response = await client.post(
                "https://api.x.ai/v1/chat/completions",
                json={
                    "messages": [{"role": "user", "content": prompt}],
                    "model": "grok-beta",
                    "temperature": 0.7,
                    "max_tokens": 500
                },
                headers={
                    "Authorization": f"Bearer {os.getenv('GROK_KEY')}",
                    "Content-Type": "application/json"
                }
            )
            data = response.json()
            answer = data["choices"][0]["message"]["content"].strip()
            return {"answer": answer}
        except Exception as e:
            return {"answer": "Grok is waking up… Try again in 5 sec!"}
