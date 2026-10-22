
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.question import controller
from src.question.schema import GenerateQuestionSchema
from src.User.db import get_db
from src.User.utils import is_authenticated
from src.User.model import TaskModel

ques_routes = APIRouter(
    prefix="/ques",
    
)


@ques_routes.post("/generate")
def generate_question(
    body: GenerateQuestionSchema,
    db: Session = Depends(get_db),
    user: TaskModel = Depends(is_authenticated)
):
    return controller.generate_question(
        interview_id=body.interview_id,
        db=db,
        user=user,
        total_questions=body.total_questions,
        show_expected_answer=body.show_expected_answer
    )
