from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import JSONResponse
import openai
from dotenv import load_dotenv
load_dotenv()

import os
openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()

@app.post("/chat/upload")
async def chat_upload(
        message: str = Form(...),
        mode: str = Form(...),
        images: list[UploadFile] = []
):
    print(f"Received: message='{message}', mode='{mode}', images={len(images)}")

    system_prompt = {
        "general": "You are a helpful plumbing assistant.",
        "sms": "You are a plumber replying to customers via SMS. Be short and friendly.",
        "mentor": "You are a master plumber mentoring a junior technician."
    }.get(mode, "You are a helpful assistant.")

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": message}
            ]
        )

        reply = response.choices[0].message.content.strip()
        tokens = response["usage"]
        return {
            "response": reply,
            "tokens": {
                "prompt": tokens["prompt_tokens"],
                "completion": tokens["completion_tokens"],
                "total": tokens["total_tokens"]
            }
        }

    except Exception as e:
        return JSONResponse(content={"response": f"Error: {str(e)}"}, status_code=500)
