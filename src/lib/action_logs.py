from sqlalchemy.ext.asyncio import AsyncSession
from src.models.action_logs import ActionLog
from src.schemas.action_logs import ActionLogCreate

async def create(db: AsyncSession, log_in: ActionLogCreate) -> ActionLog:
    new_log = ActionLog(**log_in.model_dump())
    db.add(new_log)
    await db.commit()
    await db.refresh(new_log)
    return new_log