# session_1.py  ←  FIXED FOREVER
from fastapi import FastAPI, Request
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import httpx
import json

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
                "https://router.huggingface.co/hf-inference/models/mistralai/Mistral-7B-Instruct-v0.2",
                json={"inputs": f"[INST] {prompt} [/INST]"},
                headers={"Authorization": "Bearer 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"}
            )
            result = r.json()

            # FIXED THIS PART ↓↓↓
            if isinstance(result, list) and len(result) > 0:
                text = result[0].get("generated_text", "")
            elif isinstance(result, dict) and "error" in result:
                return {"answer": f"AI busy: {result['error']}. Try again!"}
            else:
                text = json.dumps(result)

            answer = text.split("[/INST]")[-1].replace(prompt, "").strip()
            return {"answer": answer or "Thinking…"}
        except Exception as e:
            return {"answer": "AI woke up! Ask again."}

