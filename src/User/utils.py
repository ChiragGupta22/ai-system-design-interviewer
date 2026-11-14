
from fastapi import Request, HTTPException, status, Depends
from sqlalchemy.orm import Session
import jwt
from jwt.exceptions import InvalidTokenError

from src.User.settings import settings
from src.User.db import get_db
from src.User.model import TaskModel


def is_authenticated(
    req: Request,
    db: Session = Depends(get_db)
):
    auth_header = req.headers.get("Authorization")

    print("AUTH HEADER EXISTS:", bool(auth_header))

    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(
            status_code=401,
            detail="Missing or invalid Authorization header"
        )

    token = auth_header.split(" ", 1)[1].strip()

    try:
        data = jwt.decode(
            token,
            settings.SECRETE_KEY,
            algorithms=[settings.ALGORITHAM]
        )

        user_id = data.get("_id")

        print("JWT DECODE SUCCESS")
        print("USER ID:", user_id)

        user = db.query(TaskModel).filter(
            TaskModel.id == user_id
        ).first()

        print("USER FOUND:", bool(user))

        if not user:
            raise HTTPException(
                status_code=401,
                detail="User not found"
            )

        return user

    except InvalidTokenError as e:
        print("JWT ERROR:", repr(e))

        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )

# Admin authorize
def is_admin(user: TaskModel = Depends(is_authenticated)):
    if user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )

    return user
