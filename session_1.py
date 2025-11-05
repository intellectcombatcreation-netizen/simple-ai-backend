# session_1.py  ←  UNKILLABLE EDITION
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

    async with httpx.AsyncClient(timeout=60.0) as client:
        try:
            r = await client.post(
                "https://router.huggingface.co/hf-inference/models/mistralai/Mistral-7B-Instruct-v0.2",
                json={"inputs": f"[INST] {prompt} [/INST]"},
                headers={"Authorization": f"Bearer {os.getenv('HF_TOKEN')}"}
            )
            result = r.json()

            if "error" in result:
                return {"answer": f"AI says: {result['error'][:100]}… Refresh & retry!"}

            text = result[0]["generated_text"] if isinstance(result, list) else result
            answer = text.split("[/INST]")[-1].replace(prompt, "").strip()
            return {"answer": answer or "Thinking…"}
        except Exception as e:
            return {"answer": "AI is warming up! Ask again in 5 sec."}
