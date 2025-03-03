import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.chat_repository import save_conversation,get_conversation_history
from app.repositories.user_repository import create_user
from app.services.user_service import hash_password


@pytest.mark.asyncio
async def test_save_conversation_history(db: AsyncSession):
    username = "test_user2"
    email = "test2@example.com"
    password = "password123"
    hashed_password = hash_password(password)

    test_user = await create_user(db, username, email, hashed_password)
    assert test_user is not None


    user_id = test_user.id

    query = "fetch me all sources that are in .json format"
    response = ("The sources that are in .json format are only: "
                "Source path: hdfs://localhost:9000/user/sources/7.json"
                "Explanation: From all the sources examined, it is the only source in .json format")

    new_history = await save_conversation(db, query, response, user_id)

    assert new_history is not None
    assert new_history.user_id == user_id
    assert new_history.message_text == query
    assert new_history.response_text == response

@pytest.mark.asyncio
async def test_get_conversation_history(db: AsyncSession):
    username = "test_user5"
    email = "test5@example.com"
    password = "panagiotis1234"
    hashed_password = hash_password(password)

    test_user = await create_user(db, username, email, hashed_password)
    assert test_user is not None

    user_id = test_user.id
    query = "fetch me all sources that are in .json format"
    response = ("The sources that are in .json format are only: "
                "Source path: hdfs://localhost:9000/user/sources/7.json"
                "Explanation: From all the sources examined, it is the only source in .json format")
    first_history = await save_conversation(db, query, response, user_id)
    query = "fetch me all sources that are in .csv format"
    response = ("The sources that are in .csv format are only: "
                "Source path: hdfs://localhost:9000/user/sources/7.json"
                "Explanation: From all the sources examined, it is the only source in .json format")
    second_history = await save_conversation(db, query, response, user_id)
    conversation_history = await get_conversation_history(db,user_id)
    assert conversation_history is not None
    assert len(conversation_history) == 2
    assert conversation_history[0][0] == "fetch me all sources that are in .json format"
    assert conversation_history[1][0] == "fetch me all sources that are in .csv format"