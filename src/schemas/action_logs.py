from pydantic import BaseModel
from typing import Optional, Dict
from datetime import datetime

class ActionLogCreate(BaseModel):
    user_id: int
    action: str
    details: Dict
    timestamp: datetime
    details: str

class ActionLogRead(BaseModel):
    id: int
    user_id: int
    action: str
    details: Dict
    timestamp: datetime
    details: str

    class Config:
        orm_mode = True