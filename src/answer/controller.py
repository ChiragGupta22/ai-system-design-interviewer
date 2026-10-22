
from fastapi import HTTPException
from sqlalchemy.orm import Session

from src.question.models import Question
from src.answer.model import Answer
from src.interview.models import Interview


def create_answer(
    body,
    db: Session,
    user
):
    question = (
        db.query(Question)
        .filter(Question.id == body.question_id)
        .first()
    )

    if not question:
        raise HTTPException(
            status_code=404,
            detail="Question not found"
        )

    
    interview = (
        db.query(Interview)
        .filter(
            Interview.id == question.interview_id,
            Interview.user_id == user.id
        )
        .first()
    )

    if not interview:
        raise HTTPException(
            status_code=403,
            detail="You cannot answer this question"
        )

    try:
        answer = Answer(
            question_id=question.id,
            user_id=user.id,
            answer_text=body.answer_text
        )

        db.add(answer)
        db.commit()
        db.refresh(answer)

        return answer

    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Failed to save answer"
        )
