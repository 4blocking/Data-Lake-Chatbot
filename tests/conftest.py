import pytest_asyncio
import pytest
import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import async_session_maker

@pytest_asyncio.fixture(scope="function")
async def db() -> AsyncSession:
    async with async_session_maker() as session:
        yield session
        await session.rollback()

@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()
