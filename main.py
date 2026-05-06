import os
from dotenv import load_dotenv

# Load .env first
load_dotenv()

# Verify API key
if os.getenv("GEMINI_API_KEY") is None:
    raise RuntimeError("GEMINI_API_KEY not set in .env")

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from routers import chat, vision

app = FastAPI()

app.include_router(chat.router)
app.include_router(vision.router)

@app.get("/")
async def serve_ui():
    with open("code.html", "r", encoding="utf-8") as f:
        html_content = f.read()
    return HTMLResponse(content=html_content)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
