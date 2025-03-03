from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from app.models.chat_models import History
from sqlalchemy.future import select

async def save_conversation(db: AsyncSession, query: str, response: str, user_id: int):
    new_history = History(user_id=user_id,message_text=query,response_text=response)
    db.add(new_history)
    try:
        await db.commit()
        await db.refresh(new_history)
        return new_history
    except IntegrityError:
        await db.rollback()
        return None

async def get_conversation_history(db: AsyncSession, user_id: int):
    """Fetches the conversation history for a user, ordered by timestamp."""
    result = await db.execute(
        select(History.message_text, History.response_text)
        .where(History.user_id == user_id)
        .order_by(History.timestamp.asc())
    )
    history = result.all()
    return [(row[0], row[1]) for row in history]