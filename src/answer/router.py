
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.answer import controller
from src.answer.model import Answer
from src.answer.schema import AnswerCreate
from src.User.db import get_db
from src.User.utils import is_authenticated
from src.User.model import TaskModel

ans_routes = APIRouter(prefix="/answers")


@ans_routes.post("/create")
def create_answer(
    body: AnswerCreate,
    db: Session = Depends(get_db),
    user: TaskModel = Depends(is_authenticated)
):
    return controller.create_answer(body, db, user)


@ans_routes.get("/scores")
def get_scores(
    db: Session = Depends(get_db),
    user: TaskModel = Depends(is_authenticated)
):
    query = db.query(Answer)

    if user.role != "admin":
        query = query.filter(Answer.user_id == user.id)

    answers = query.order_by(Answer.id.desc()).all()

    return [
        {
            "user_id": answer.user_id,
            "question_id": answer.question_id,
            "marks": answer.marks
        }
        for answer in answers
    ]
