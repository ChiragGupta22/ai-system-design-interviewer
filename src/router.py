from fastapi import APIRouter, Depends,status,Request
from sqlalchemy.orm import Session
from src.db import get_db
from src.schema import UserSchema , UserResponseSchema,LoginSchema
from src import controller
from src.utils import is_authenticated
from src.model import TaskModel

user_routes = APIRouter(prefix="/user")


@user_routes.post("/register",response_model= UserResponseSchema,status_code=status.HTTP_201_CREATED)
def register(body: UserSchema, db: Session = Depends(get_db)):
    return controller.register(body, db)


@user_routes.post("/login", status_code=status.HTTP_200_OK)
def login(body: LoginSchema, db: Session = Depends(get_db)):
    return controller.login_user(body, db)

@user_routes.get("/is_auth",status_code=status.HTTP_200_OK,response_model=UserResponseSchema)
def is_auth(req:Request,db: Session = Depends(get_db)):
    return controller.is_authenticated(req,db)