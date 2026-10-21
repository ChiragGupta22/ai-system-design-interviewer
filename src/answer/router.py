
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.answer import controller
from src.answer.schema import AnswerCreate
from src.User.db import get_db
from src.User.utils import is_authenticated
from src.User.model import TaskModel

ans_routes = APIRouter(prefix="/answers", tags=["Answers"])


@ans_routes.post("/create")
def create_answer(
    body: AnswerCreate,
    db: Session = Depends(get_db),
    user: TaskModel = Depends(is_authenticated)
):
    return controller.create_answer(body, db, user)
