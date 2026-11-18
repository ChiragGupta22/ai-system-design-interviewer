
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.User.db import get_db
from src.User.utils import is_authenticated
from src.User.model import TaskModel

from src.admin import service


admin_routes = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)


# Admin authorization
def is_admin(
    user: TaskModel = Depends(is_authenticated)
):
    if user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )

    return user


# Get all users
@admin_routes.get("/users")
def get_all_users(
    db: Session = Depends(get_db),
    admin: TaskModel = Depends(is_admin)
):
    return service.get_all_users(db)


# Get single user
@admin_routes.get("/users/{user_id}")
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    admin: TaskModel = Depends(is_admin)
):
    return service.get_user(user_id, db)


# Get all users' marks
@admin_routes.get("/marks")
def get_all_marks(
    db: Session = Depends(get_db),
    admin: TaskModel = Depends(is_admin)
):
    return service.get_all_marks(db)


# Get specific user's marks
@admin_routes.get("/marks/{user_id}")
def get_user_marks(
    user_id: int,
    db: Session = Depends(get_db),
    admin: TaskModel = Depends(is_admin)
):
    return service.get_user_marks(user_id, db)
