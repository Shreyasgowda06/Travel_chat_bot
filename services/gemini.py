import os
import time
import google.generativeai as genai
from google.api_core import exceptions

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

SYSTEM_INSTRUCTION = """
You are TravelWith AI, a knowledgeable and friendly travel assistant. 
You help users with destination discovery, itinerary planning, budget estimation, 
visa and documentation requirements, transport options, accommodation, local food, 
and cultural experiences.

Answer general travel questions confidently. Add brief disclaimers only where 
genuinely appropriate (e.g. visa rules change — verify with the official embassy). 
Do NOT refuse routine travel questions.

Refuse only: requests clearly unrelated to travel, harmful or dangerous instructions, 
and requests for personalised medical or legal advice. 
For borderline questions, answer the travel-relevant part and note any limitations.
"""

def generate_chat_response(history: list[dict]) -> str:
    model = genai.GenerativeModel(
        model_name="gemini-2.5-flash-lite",
        system_instruction=SYSTEM_INSTRUCTION
    )
    
    try:
        response = model.generate_content(history)
        return response.text
    except exceptions.ResourceExhausted:
        time.sleep(2)
        try:
            response = model.generate_content(history)
            return response.text
        except exceptions.ResourceExhausted:
            return "I'm a little busy right now — please try again in a moment."
    except exceptions.PermissionDenied as e:
        return str(e)
    except exceptions.GoogleAPIError as e:
        return str(e)
    except Exception as e:
        print(f"Error in chat: {e}")
        return "Something went wrong, please retry."

def generate_vision_response(prompt: str, image_bytes: bytes, mime_type: str) -> str:
    model = genai.GenerativeModel(
        model_name="gemini-2.5-flash-lite",
        system_instruction=SYSTEM_INSTRUCTION
    )
    
    contents = [
        {"mime_type": mime_type, "data": image_bytes},
        prompt
    ]
    
    try:
        response = model.generate_content(contents)
        return response.text
    except exceptions.ResourceExhausted:
        time.sleep(2)
        try:
            response = model.generate_content(contents)
            return response.text
        except exceptions.ResourceExhausted:
            return "I'm a little busy right now — please try again in a moment."
    except exceptions.PermissionDenied as e:
        return str(e)
    except exceptions.GoogleAPIError as e:
        return str(e)
    except Exception as e:
        print(f"Error in vision: {e}")
        return "Something went wrong, please retry."
