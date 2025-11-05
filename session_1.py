from fastapi import FastAPI, Request
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import httpx
import os

app = FastAPI()

# ✅ CORS FIX (required for frontend to call backend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Serve your HTML file
@app.get("/")
async def serve_home():
    return FileResponse("session_1.html")


# ✅ HF Endpoint
HF_URL = "https://router.huggingface.co/hf-inference/models/google/flan-t5-large"


@app.post("/api/ai")
async def ai(request: Request):
    body = await request.json()
    prompt = body.get("prompt", "")

    # ✅ Load token
    token = os.getenv("HF_TOKEN")
    if not token:
        print("ERROR: HF_TOKEN not found in environment!")
        return {"answer": "Backend error: HF token missing"}

    async with httpx.AsyncClient(timeout=80) as client:
        try:
            # ✅ Make HF request
            r = await client.post(
                HF_URL,
                json={"inputs": f"Compare phones: {prompt}"},
                headers={"Authorization": f"Bearer {token}"},
            )

            print("\n--------- HF RAW RESPONSE ---------")
            print(r.text)
            print("----------------------------------\n")

            result = r.json()

            # ✅ HF sometimes returns dict, sometimes list
            if isinstance(result, list) and "generated_text" in result[0]:
                return {"answer": result[0]["generated_text"].strip()}

            # ✅ Send full error to frontend if HF fails
            return {"answer": f"HF Error: {result}"}

        except Exception as e:
            print("ERROR:", e)
            return {"answer": "Backend error: HF request failed"}

