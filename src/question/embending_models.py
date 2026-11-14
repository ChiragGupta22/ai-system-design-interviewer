
from sqlalchemy import Column, Integer, ForeignKey
from pgvector.sqlalchemy import Vector

from src.User.db import Base


class ExpectedAnswerEmbedding(Base):
    __tablename__ = "expected_answer_embeddings"

    id = Column(Integer, primary_key=True, index=True)

    question_id = Column(
        Integer,
        ForeignKey("questions.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
        index=True
    )

    embedding = Column(Vector(384), nullable=False)
