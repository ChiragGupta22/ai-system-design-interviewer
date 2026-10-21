from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.User.db import get_db
from src.User.utils import is_authenticated
from src.question.models import Question
from src.answer.model import Answer


router = APIRouter(prefix="/answers")


@router.post("/evaluate/{question_id}")
def evaluate_answer(
    question_id: int,
    db: Session = Depends(get_db),
    user=Depends(is_authenticated)
):
    question = db.query(Question).filter(
        Question.id == question_id
    ).first()

    if not question:
        raise HTTPException(
            status_code=404,
            detail="Question not found"
        )

    answer = db.query(Answer).filter(
        Answer.question_id == question_id,
        Answer.user_id == user.id
    ).order_by(Answer.id.desc()).first()

    if not answer:
        raise HTTPException(
            status_code=404,
            detail="Answer not found"
        )

    result = compare_answers(
        question.expected_answer,
        answer.answer_text
    )

    return {
        "question_id": question.id,
        "expected_answer": question.expected_answer,
        "candidate_answer": answer.answer_text,
        "evaluation": result
    }