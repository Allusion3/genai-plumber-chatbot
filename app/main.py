from fastapi import FastAPI, Form, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import openai
import os
import base64
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
client = openai.OpenAI()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/chat/upload")
async def chat_upload(
        message: str = Form(...),
        mode: str = Form(...),
        image: UploadFile = File(None)  # Optional image file
):
    print(f"Received message: {message}")
    print(f"Mode: {mode}")
    print(f"Image: {image.filename if image else 'None'}")

    # Set system prompt
    if mode == "sms":
        system_prompt = "You're a plumber sending short SMS replies to customers."
    elif mode == "mentor":
        system_prompt = "You're mentoring a junior plumber with helpful tips."
    else:
        system_prompt = "You're a helpful plumber answering customer questions."

    messages = [{"role": "system", "content": system_prompt}]

    if image:
        # Read and encode image
        image_bytes = await image.read()
        image_base64 = base64.b64encode(image_bytes).decode("utf-8")

        # Detect MIME type (fix for png/jpg issues)
        mime_type = image.content_type or "image/png"  # fallback

        print(f"MIME type: {mime_type}")
        print(f"Base64 starts with: {image_base64[:30]}")

        messages.append({
            "role": "user",
            "content": [
                {"type": "text", "text": message},
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:{mime_type};base64,{image_base64}"
                    }
                }
            ]
        })
    else:
        messages.append({"role": "user", "content": message})

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # gpt-4-vision-preview, gpt-3.5-turbo for testing
            messages=messages,
            max_tokens=800,
            timeout=20
        )

        reply = response.choices[0].message.content.strip()
        usage = response.usage

        print("GPT-4 Vision reply sent.")

        return {
            "response": reply,
            "tokens": {
                "prompt": usage.prompt_tokens,
                "completion": usage.completion_tokens,
                "total": usage.total_tokens
            }
        }

    except Exception as e:
        print(f"OpenAI API error: {e}")
        return {"error": str(e)}
