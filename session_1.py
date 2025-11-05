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

    async with httpx.AsyncClient(timeout=60) as client:
        try:
            r = await client.post(
                "https://api-inference.huggingface.co/models/google/flan-t5-large",
                json={"inputs": f"Compare phones: {prompt}"},
                headers={"Authorization": f"Bearer {os.getenv('HF_TOKEN')}"}
            )
            result = r.json()
            answer = result[0]["generated_text"] if isinstance(result, list) else str(result)
            return {"answer": answer.strip()}
        except:
            return {"answer": "AI is ready! Ask again."}
