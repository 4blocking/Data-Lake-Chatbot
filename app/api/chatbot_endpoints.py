from fastapi import APIRouter, HTTPException, Depends

from app.core.security import get_current_user
from app.services.chat_service import process_chat_query
from pydantic import BaseModel

router = APIRouter()

# Request model
class ChatRequest(BaseModel):
    query: str

# Chatbot endpoint
@router.post("/chat")
def chat(request: ChatRequest, user = Depends(get_current_user)):
    """Handles chatbot queries and returns AI-generated responses."""
    response = process_chat_query(request.query)
    if not response:
        raise HTTPException(status_code=400, detail="Failed to generate response.")
    return {"response": response}


