from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.user_repository import create_user, get_user_by_username, get_user_by_email
from app.services.user_service import hash_password, verify_password
from app.core.security import create_access_token
from app.core.database import get_db
from pydantic import BaseModel
from datetime import timedelta

router = APIRouter()


# Request Model
class UserRegister(BaseModel):
    username: str
    email: str
    password: str

# Request Model
class UserLogin(BaseModel):
    username: str
    password: str


@router.post("/register")
async def register(user_data: UserRegister, db: AsyncSession = Depends(get_db)):
    """Registers a new user with a hashed password."""

    # Check if username or email already exists
    existing_user = await get_user_by_username(db, user_data.username)
    existing_email = await get_user_by_email(db, user_data.email)

    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists.")
    if existing_email:
        raise HTTPException(status_code=400, detail="Email already registered.")

    hashed_password = hash_password(user_data.password)

    user = await create_user(db, user_data.username, user_data.email, hashed_password)
    if not user:
        raise HTTPException(status_code=500, detail="User registration failed.")

    return {"message": "Registration successful."}


@router.post("/login")
async def login(user_data: UserLogin, db: AsyncSession = Depends(get_db)):
    """Authenticates user and returns JWT token."""

    user = await get_user_by_username(db, user_data.username)
    if not user or not verify_password(user_data.password, user.password):
        raise HTTPException(status_code=400, detail="Invalid username or password.")

    # Generate JWT token
    access_token_expires = timedelta(minutes=60)
    access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)

    return {"access_token": access_token, "token_type": "bearer"}
