from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.User.db import Base, engine
from src.User.router import user_routes
from src.interview.router import task_routes
from src.question.router import ques_routes
from src.answer.router import ans_routes

Base.metadata.create_all(engine)

app = FastAPI()

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://frontend-system-design-interviewer.vercel.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(ques_routes)
app.include_router(task_routes)
app.include_router(user_routes)
app.include_router(ans_routes)