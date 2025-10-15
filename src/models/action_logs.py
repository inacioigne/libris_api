from src.db.database import Base
from sqlalchemy import Column, Integer, String, DateTime, func, ForeignKey, JSON
from sqlalchemy.orm import relationship

class ActionLog(Base):
    __tablename__ = "action_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    action = Column(String(255), nullable=False)
    timestamp = Column(DateTime, server_default=func.now())
    details = Column(JSON, nullable=True)

    user = relationship("User", backref="action_logs", lazy="joined")