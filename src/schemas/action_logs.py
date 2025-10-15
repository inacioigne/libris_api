from pydantic import BaseModel
from typing import Optional, Any

class ActionLogCreate(BaseModel):
    user_id: int
    action: str
    details: Optional[Any] = None  # aceita dict/string
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None