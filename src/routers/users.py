from fastapi import APIRouter, status, Depends, HTTPException
from src.db.database import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from src.schemas.users import UserCreate, UserRead
from src.lib import users

router = APIRouter(prefix="/users", tags=["users"])

@router.post(
        "/", 
        status_code=status.HTTP_201_CREATED,
        response_model=UserRead
        )
async def create_user(user_in: UserCreate, db: AsyncSession = Depends(get_session)):

    existing_user = await users.get_by_email(user_in.email, db)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    user = await users.create(user_in, db)

    return user