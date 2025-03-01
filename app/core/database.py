from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
import os

DB_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://vboxuser:changeme@localhost:5432/datalakes")


engine = create_async_engine(DB_URL, echo=True)

# Create async session factory
async_session_maker = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Define Declarative Base for ORM models
class Base(DeclarativeBase):
    pass

# Dependency to get DB session
async def get_db():
    async with async_session_maker() as session:
        yield session
