from src.schemas.users import UserCreate
from src.models.users import User
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select

async def create(user_in: UserCreate, db: AsyncSession ):

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

async def get_by_email(email: str, db: AsyncSession):

    q = select(User).where(User.email == email)
    result = await db.execute(q)
    user = result.scalars().first()
    
    return user