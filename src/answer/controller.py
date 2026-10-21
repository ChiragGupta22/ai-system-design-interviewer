
from sqlalchemy import Column, Integer, Text, ForeignKey
from src.User.db import Base


class Answer(Base):
    __tablename__ = "answers"

    id = Column(Integer, primary_key=True, index=True)

    question_id = Column(
        Integer,
        ForeignKey("questions.id"),
        nullable=False,
        index=True
    )

    user_id = Column(
        Integer,
        ForeignKey("user_tasks.id"),
        nullable=False,
        index=True
    )

    answer_text = Column(Text, nullable=False)
