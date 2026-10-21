from fastapi import FastAPI
from src.User.db import Base, engine
from src.User.router import user_routes
from src.interview.router import task_routes
from src.question.router import ques_routes
Base.metadata.create_all(engine)

app = FastAPI()

app.include_router(ques_routes)
app.include_router(task_routes)
app.include_router(user_routes)