from fastapi import FastAPI, Request
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import httpx

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"])

@app.get("/")
async def root():
    return FileResponse("session_1.html")

@app.post("/api/ai")
async def ai(request: Request):
    body = await request.json()
    prompt = body.get("prompt", "Hi")
    async with httpx.AsyncClient() as client:
        r = await client.post(
            "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2",
            json={"inputs": f"[INST] {prompt} [/INST]"},
            headers={"Authorization": "Bearer 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"}
        )
        answer = r.json()[0]["generated_text"].split("[/INST]")[-1].strip()
        return {"answer": answer}