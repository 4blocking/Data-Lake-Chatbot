import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.user_repository import create_user, get_user_by_username, get_user_by_email
from app.services.user_service import hash_password

@pytest.mark.asyncio
async def test_registration_success(db: AsyncSession):
    """Test successful registration."""
    username = "testtttt"
    email = "email"
    password = "password"
    hashed_password = hash_password(password)
    new_user = await create_user(db, username, email, hashed_password)
    assert new_user is not None
    assert new_user.username == username
    assert new_user.email == email
    assert new_user.password != password

@pytest.mark.asyncio
async def test_get_user_by_username(db: AsyncSession):
    """Test get user by username."""
    query_username = "testtttt"
    another_one = "test"
    existing_user = await get_user_by_username(db, query_username)
    assert existing_user is not None
    second_user = await get_user_by_username(db, another_one)
    assert second_user is None

@pytest.mark.asyncio
async def test_get_user_by_email(db: AsyncSession):
    """Test get user by email."""
    query_email = "email"
    another_one = "test"
    existing_user = await get_user_by_email(db, query_email)
    assert existing_user is not None
    second_user = await get_user_by_email(db, another_one)
    assert second_user is None


