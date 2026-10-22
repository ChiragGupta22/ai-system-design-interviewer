
from sqlalchemy import Column, Integer, Text, ForeignKey
from src.User.db import Base


class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)

    interview_id = Column(
        Integer,
        ForeignKey("interviews.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    question_text = Column(Text, nullable=False)

    expected_answer = Column(Text, nullable=False)


class ExpectedConcept(Base):
    __tablename__ = "expected_concepts"

    id = Column(Integer, primary_key=True, index=True)

    question_id = Column(
        Integer,
        ForeignKey("questions.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    concept = Column(Text, nullable=False)
