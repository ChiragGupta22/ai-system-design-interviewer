from sqlalchemy import Column, Integer, String, ForeignKey
from src.User.db import Base
class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    interview_id = Column(
        Integer,
        ForeignKey("interviews.id", ondelete="CASCADE")
    )
    question_text = Column(String, nullable=False)
    expected_answer = Column(String, nullable=False)