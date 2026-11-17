
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.User.db import Base, engine
from src.User.router import user_routes
from src.interview.router import task_routes
from src.question.router import ques_routes
from src.answer.router import ans_routes

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://frontend-system-design-interviewer.vercel.app",
        "http://localhost:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "AI Interviewer Backend is Running"}

app.include_router(ques_routes)
app.include_router(task_routes)
app.include_router(user_routes)
app.include_router(ans_routes)
