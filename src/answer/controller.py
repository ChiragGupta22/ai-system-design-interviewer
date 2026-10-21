
from fastapi import HTTPException
from sqlalchemy.orm import Session

from src.question.models import Question
from src.answer.model import Answer
from src.User.model import TaskModel
from src.answer.schema import AnswerCreate


def create_answer(
    body: AnswerCreate,
    db: Session,
    user: TaskModel
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

    # Check whether the question belongs to this user
    from src.interview.models import Interview

    interview = (
        db.query(Interview)
        .filter(Interview.id == question.interview_id)
        .first()
    )

    if not interview or interview.user_id != user.id:
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

    return {
        "message": "Answer saved successfully",
        "id": answer.id,
        "question_id": answer.question_id,
        "user_id": answer.user_id,
        "answer_text": answer.answer_text
    }
