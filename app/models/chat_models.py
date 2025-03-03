from sqlalchemy import Column, DateTime, func, Integer, ForeignKey, Text
from app.core.database import Base

"""
map user's conversation history with the chatbot in db
class History:
   history_id : Int, primary key
   user_id : Int, Foreign key references user model
   message_text : Text
   response_text : Text
   timestamp : DateTime
"""
class History(Base):
    __tablename__ = 'history'
    history_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    message_text = Column(Text, nullable=False)
    response_text = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=func.now())