from src.User.schema import UserSchema,LoginSchema
from sqlalchemy.orm import Session
from src.User.model import TaskModel
from fastapi import HTTPException ,status,Request
from pwdlib import PasswordHash
from src.User.settings import settings
from datetime import datetime,timedelta
import jwt


password_hash = PasswordHash.recommended()

def verify_password(plain_password, hashed_password) :
    return password_hash.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return password_hash.hash(password)


def register(body: UserSchema, db: Session):
    is_user = db.query(TaskModel).filter(
        TaskModel.email == body.email
    ).first()

    if is_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    hashed_password = get_password_hash(body.password)

    new_user = TaskModel(
        name=body.name,
        email=body.email,
        hashed_password=hashed_password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "msg": "Registration successful",
         "id": new_user.id,
        "name": new_user.name,
        "email": new_user.email,
        
    }



def login_user(body: LoginSchema, db: Session):
    user = db.query(TaskModel).filter(
        TaskModel.email == body.email
    ).first()

    if not user or not verify_password(
        body.password, user.hashed_password
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    exp_time = datetime.now() + timedelta(
        minutes=settings.EXP_TIME
    )

    token = jwt.encode(
        {"_id": user.id, "exp": exp_time},
        settings.SECRETE_KEY,
        algorithm=settings.ALGORITHAM
    )

    return {"token": token}
