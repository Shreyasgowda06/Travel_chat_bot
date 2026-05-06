from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Dict, Any
from services.gemini import generate_chat_response

router = APIRouter()

class ChatRequest(BaseModel):
    messages: List[Dict[str, Any]]

@router.post("/chat")
async def chat_endpoint(request: ChatRequest):
    reply = generate_chat_response(request.messages)
    return {"reply": reply}
