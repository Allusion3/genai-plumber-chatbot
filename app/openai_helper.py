import openai
import os
from dotenv import load_dotenv
from prompt_helper import PromptHelper

# Load environment variables from a .env file
load_dotenv()

# Set the OpenAI API key from the environment variables
openai.api_key = os.getenv("OPENAI_API_KEY")

# Create a client instance for the OpenAI SDK
client = openai.OpenAI()

class OpenAIHelper:
    def __init__(self):
        # Ensure the API key is available; raise an error if not found
        if not openai.api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables.")

    def get_reply(self, message: str, mode: str = "general") -> dict:
        prompt_helper = PromptHelper()
        system_prompt = prompt_helper.get_prompt(mode)

        # Call the OpenAI API to generate a chat completion
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # Specify the model to use
            messages=[
                {"role": "system", "content": system_prompt},  # System prompt to set the AI's behavior
                {"role": "user", "content": message}  # User's input message
            ]
        )

        # Extract the AI's reply from the response
        reply = response.choices[0].message.content.strip()

        # Extract token usage details from the response
        tokens = response.usage

        # Return the reply and token usage as a dictionary
        return {
            "response": reply,
            "tokens": {
                "prompt": tokens.prompt_tokens,  # Tokens used for the prompt
                "completion": tokens.completion_tokens,  # Tokens used for the AI's reply
                "total": tokens.total_tokens  # Total tokens used in the request
            }
        }