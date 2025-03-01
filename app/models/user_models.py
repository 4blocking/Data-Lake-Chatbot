from sqlalchemy import Column, String, DateTime, func, Integer
from app.core.database import Base

"""
map users that utilize the chatbot in db
class User:
    id Int
    username String unique
    email String unique
    password String (hashed)
    created_at datetime
"""
class User(Base):
    __tablename__ ='users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True, nullable=False, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    password = Column(String, nullable=False)
    created_at = Column(DateTime, default=func.now())
