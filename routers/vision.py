from fastapi import APIRouter, UploadFile, File, Form
from services.gemini import generate_vision_response

router = APIRouter()

@router.post("/vision")
async def vision_endpoint(prompt: str = Form(...), image: UploadFile = File(...)):
    image_bytes = await image.read()
    mime_type = image.content_type
    reply = generate_vision_response(prompt, image_bytes, mime_type)
    return {"reply": reply}
