from fastapi import APIRouter,Depends
from src.question import controller
from src.question.schema import questionSchema
from src.User.db import get_db
from src.User.utils import is_authenticated
from src.User.model import TaskModel
ques_routes = APIRouter(prefix="/ques")

@ques_routes.post("/create")
def create_question(
    body:questionSchema,
    db=Depends(get_db),
    user: TaskModel = Depends(is_authenticated)
):
    return controller.create_question(body, db, user)