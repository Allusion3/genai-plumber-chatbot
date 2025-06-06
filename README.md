#  Plumber GenAI Chatbot (GPT-4 Vision + GPT-3.5 Turbo)

This project is a FastAPI-powered backend that uses OpenAI's GPT models to create a chatbot assistant for plumbing-related use cases. Users can submit a message and (optionally) an image, and receive a smart, role-specific response from the assistant.

### It supports:
- Text-only questions using `gpt-3.5-turbo` for fast, cheap testing
- Image + text requests using `gpt-4-vision-preview` for real-world analysis
- Multiple chatbot "modes" like customer replies, technician mentorship, and general plumbing help

---

## Features

- Text input support for GPT-3.5 and GPT-4
- Optional image upload processed by GPT-4 Vision
- Multiple assistant modes:
  - `general`: helpful plumber assistant
  - `sms`: short, customer-facing responses
  - `mentor`: mentor-style advice to junior techs
- Clean structure using helper classes for prompts and OpenAI logic
- Includes built-in token usage reporting
- Debug tip for Windows users with stuck Python processes

---

## Getting Started

### 1. Clone the repo
```bash
git clone https://github.com/Allusion3/plumber-genai
cd plumber-genai
```
### 2. Install dependencies
```bash
pip install -r requirements.txt
```
### 3. Set up your OpenAI API key
Create a .env file in the root directory and add your OpenAI API key:
```bash
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```
### 4. Run the FastAPI server
```bash
uvicorn app.main:app --reload
```
Access the application at http://127.0.0.1:8000.

## Troubleshooting
### Common Issue: Repeated Errors During Testing
If you encounter the same error repeatedly while testing, it may be due to lingering Python processes. Follow these steps to resolve the issue:


1. Press **Ctrl + Alt + Delete** and open the Task Manager.
2. Look for any running Python instances in the "Processes" tab.
3. End all Python processes.
4. Restart your testing.

### Other Issues
- Ensure your **.env** file is correctly configured with your OpenAI API key.
- Verify that all dependencies are installed using **pip install -r requirements.txt.**

## Dependencies
The application uses the following Python libraries:


- **fastapi**: For building the web application.
- **python**-dotenv: For loading environment variables.
- **openai**: For interacting with OpenAI's API.
- **uvicorn**: For running the FastAPI server.