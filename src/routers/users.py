from datetime import datetime
from fastapi import APIRouter, status, Depends
from src.db.database import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from src.schemas.users import UserCreate, UserRead
from src.models.users import User

router = APIRouter(prefix="/users", tags=["users"])

@router.post(
        "/", 
        status_code=status.HTTP_201_CREATED,
        response_model=UserRead
        )
async def create_user(user_in: UserCreate, db: AsyncSession = Depends(get_session)):
    user_in.created_at = user_in.created_at or datetime.now()
    user = User(**user_in.model_dump())
    db.add(user)
    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise

    await db.refresh(user)

    return user
    

    # user = user_in.model_dump()
    # user['id'] = 1  # Placeholder for actual DB-generated ID
    

    # return user