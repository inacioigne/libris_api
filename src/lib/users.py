from src.core.security import get_password_hash
from src.schemas.action_logs import ActionLogCreate
from src.schemas.users import UserCreate
from src.models.users import User
from src.models.action_logs import ActionLog
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select

async def create(user_in: UserCreate, db: AsyncSession ):

    hashed_password = get_password_hash(user_in.password)
    user_in.password = hashed_password
    user_in.created_at = user_in.created_at or datetime.now()
    
    user = User(**user_in.model_dump())
    db.add(user)
    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise
    await db.refresh(user)

    # log_in = ActionLog(
    #     user_id=user.id,
    #     action='register',
    #     timestamp=user_in.created_at
    # )
    # db.add(log_in)
    # try:
    #     await db.commit()
    # except IntegrityError:
    #     await db.rollback()
    #     raise
    # await db.refresh(user)

    return user

async def get_by_email(email: str, db: AsyncSession):

    q = select(User).where(User.email == email)
    result = await db.execute(q)
    user = result.scalars().first()
    
    return user