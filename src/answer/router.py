
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.User.db import get_db
from src.question.models import Question
from src.answer.model import Answer
from src.answer.schema import AnswerCreate, AnswerResponse
from src.User.utils import is_authenticated


router = APIRouter(prefix="/answers", tags=["Answers"])


@router.post("/", response_model=AnswerResponse)
def create_answer(
    body: AnswerCreate,
    db: Session = Depends(get_db),
    user=Depends(is_authenticated),
):
    question = db.query(Question).filter(
        Question.id == body.question_id
    ).first()

    if not question:
        raise HTTPException(
            status_code=404,
            detail="Question not found"
        )

    answer = Answer(
        question_id=question.id,
        user_id=user.id,
        answer_text=body.answer_text
    )

    db.add(answer)
    db.commit()
    db.refresh(answer)

    return answer
