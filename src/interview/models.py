from sqlalchemy import Column, Integer, String, ForeignKey
from src.User.db import Base

class Interview(Base):
    __tablename__ = "interviews"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(
        Integer,
        ForeignKey("user_tasks.id", ondelete="CASCADE")
    )
    project_name = Column(String)
    duration = Column(Integer, default=30)
    status = Column(String, default="in_progress")