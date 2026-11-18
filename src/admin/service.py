
from fastapi import HTTPException

from src.User.model import TaskModel
from src.interview.models import Interview
from src.answer.model import Answer
from src.question.models import Question


# Get all registered users
def get_all_users(db):

    users = db.query(TaskModel).all()

    return [
        {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "role": user.role
        }
        for user in users
    ]


# Get single user
def get_user(user_id, db):

    user = db.query(TaskModel).filter(
        TaskModel.id == user_id
    ).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "role": user.role
    }


# Get all users' marks
def get_all_marks(db):

    results = (
        db.query(Answer, TaskModel, Interview)
        .join(TaskModel, Answer.user_id == TaskModel.id)
        .join(Question, Answer.question_id == Question.id)
        .join(Interview, Question.interview_id == Interview.id)
        .order_by(Answer.id.desc())
        .all()
    )

    return [
        {
            "user_id": user.id,
            "user_name": user.name,
            "email": user.email,
            "interview_id": interview.id,
            "project_name": interview.project_name,
            "question_id": answer.question_id,
            "marks": answer.marks
        }
        for answer, user, interview in results
    ]


# Get specific user's marks
def get_user_marks(user_id, db):

    user = db.query(TaskModel).filter(
        TaskModel.id == user_id
    ).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    results = (
        db.query(Answer, Interview)
        .join(Question, Answer.question_id == Question.id)
        .join(Interview, Question.interview_id == Interview.id)
        .filter(Answer.user_id == user_id)
        .order_by(Answer.id.desc())
        .all()
    )

    return [
        {
            "user_id": user.id,
            "user_name": user.name,
            "interview_id": interview.id,
            "project_name": interview.project_name,
            "question_id": answer.question_id,
            "marks": answer.marks
        }
        for answer, interview in results
    ]
