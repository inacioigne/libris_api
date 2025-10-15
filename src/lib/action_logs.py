from sqlalchemy.ext.asyncio import AsyncSession
from src.models.action_logs import ActionLog

async def create(db: AsyncSession, log_in: ActionLogCreate, action: str, details: dict = None) -> ActionLog:
    new_log = ActionLog(user_id=user_id, action=action, details=details)
    db.add(new_log)
    await db.commit()
    await db.refresh(new_log)
    return new_log