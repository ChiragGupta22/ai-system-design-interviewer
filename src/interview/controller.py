from fastapi import HTTPException
from src.interview.schemas import InterviewSchema
from src.interview.models import Interview
from sqlalchemy.orm import Session
from src.User.model import TaskModel

def create_task(body: InterviewSchema, db: Session, user: TaskModel):
    data = body.model_dump()

    new_interview = Interview(
        **data,
        user_id=user.id
    )

    db.add(new_interview)
    db.commit()
    db.refresh(new_interview)

    return {
        "message": "Interview created successfully",
        "id": new_interview.id,
        "project_name": new_interview.project_name,
        "status": new_interview.status,
        "user_id": new_interview.user_id
    }

def get_all_task(db: Session):
    return db.query(Interview).all()

def get_tasks(db: Session, user: TaskModel):
    tasks = (
        db.query(Interview)
        .filter(Interview.user_id == user.id)
        .all()
    )

    if not tasks:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    return tasks

def get_one_task(task_id: int, db: Session, user: TaskModel):
    one_task = db.query(Interview).get(task_id)

    if not one_task:
        raise HTTPException(404, detail="Task not found")

    if one_task.user_id != user.id:
        raise HTTPException(404, detail="Task not found")

    return {
        "status": "Task Fetched Successfully",
        "data": one_task
    }


def delete_task(task_id: int, db: Session, user: TaskModel):
    one_task = db.query(Interview).get(task_id)

    if not one_task:
        raise HTTPException(404, detail="Task not found")

    if one_task.user_id != user.id:
        raise HTTPException(404, detail="Task not found")

    db.delete(one_task)
    db.commit()

    return {"status": "Task deleted Successfully"}