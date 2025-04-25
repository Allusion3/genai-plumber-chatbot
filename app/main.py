from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from openai_helper import OpenAIHelper

# Create OpenAI helper instance
ai = OpenAIHelper()

# Set up FastAPI app
app = FastAPI()

# Allow frontend calls (update origins if needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can restrict this to ["http://localhost:3000"] if needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Basic working test route (no OpenAI)
@app.post("/test-reply")
async def test_reply(
        message: str = Form(...),
        mode: str = Form(...)
):
    print(f"TEST: message='{message}', mode='{mode}'")
    return {"response": f"You said: {message} (mode: {mode})"}

# Real route that hits OpenAI
@app.post("/chat/upload")
async def chat_upload(
        message: str = Form(...),
        mode: str = Form(...),
        images: list[UploadFile] = []
):
    print(f"Received: message='{message}', mode='{mode}', images={len(images)}")

    try:
        result = ai.get_reply(message, mode)
        return result
    except Exception as e:
        import traceback
        traceback.print_exc()
        return JSONResponse(content={"response": f"Error: {str(e)}"}, status_code=500)
