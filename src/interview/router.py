from fastapi import APIRouter,Depends
from src.interview import controller
from src.interview.schemas import InterviewSchema
from src.User.db import get_db
from src.User.utils import is_authenticated
from src.User.model import TaskModel
task_routes = APIRouter(prefix="/ai")

@task_routes.post("/create")
def create_task(body:InterviewSchema,db = Depends(get_db), user:TaskModel = Depends(is_authenticated)):
    return controller.create_task(body,db,user)

@task_routes.get("/all_routes")
def get_all_task(db = Depends(get_db),user:TaskModel = Depends(is_authenticated)):
    return controller.get_all_task(db)

@task_routes.get("/all")
def get_tasks(db = Depends(get_db),user:TaskModel = Depends(is_authenticated)):
    return controller.get_tasks(db,user)


@task_routes.get("/one_tasks/{task_id}")
def get_one_task(task_id:int,db = Depends(get_db),user:TaskModel = Depends(is_authenticated)):
    return controller.get_one_task(task_id,db,user)

@task_routes.delete("/delete_tasks/{task_id}")
def delete_task(task_id:int,db = Depends(get_db),user:TaskModel = Depends(is_authenticated)):  
    return controller.delete_task(task_id,db,user)

@task_routes.post("/start")
def start_interview(
    body: InterviewSchema,
    db=Depends(get_db),
    user: TaskModel = Depends(is_authenticated)
):
    return controller.start_interview(body, db, user)