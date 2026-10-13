from fastapi import Request,HTTPException,status,Depends
from src.User.settings import settings
from sqlalchemy.orm import Session
import jwt
from src.User.db import get_db
from jwt.exceptions import InvalidTokenError
from src.User.model import TaskModel
from jwt.exceptions import InvalidTokenError

def is_authenticated(req: Request, db: Session = Depends(get_db)):
    try:
        auth_header = req.headers.get("Authorization")

        if not auth_header or not auth_header.startswith("Bearer "):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="You are unauthorized"
            )

        token = auth_header.split(" ", 1)[1].strip()

        data = jwt.decode(
            token,
            settings.SECRETE_KEY,
            algorithms=[settings.ALGORITHAM]
        )

        user_id = data.get("_id")

        user = db.query(TaskModel).filter(
            TaskModel.id == user_id
        ).first()

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="You are unauthorized"
            )

        return user

    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )
