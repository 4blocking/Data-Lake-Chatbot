from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import get_current_user
from app.services.chat_service import process_chat_query
from app.repositories.chat_repository import save_conversation,get_conversation_history
from pydantic import BaseModel

router = APIRouter()

# Request model
class ChatRequest(BaseModel):
    query: str

# Chatbot endpoint
@router.post("/chat")
async def chat(request: ChatRequest, user = Depends(get_current_user) ,db: AsyncSession = Depends(get_db)):
    """Handles chatbot queries and returns AI-generated responses."""
    response = process_chat_query(request.query)
    if not response:
        raise HTTPException(status_code=400, detail="Failed to generate response.")
    await save_conversation(db,request.query,response,user.id)
    return {"response": response}

@router.get("/history")
async def conversation_history(user = Depends(get_current_user) ,db: AsyncSession = Depends(get_db)):
    history = await get_conversation_history(db, user.id)
    if not history:
        return {"response": []}
    return {"history" : [{"message" : h[0], "response" : h[1]} for h in history]}