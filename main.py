print("STEP 1: Starting", flush=True)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

print("STEP 2: FastAPI imported", flush=True)

from src.User.db import Base, engine
print("STEP 3: Database imported", flush=True)

from src.User.router import user_routes
print("STEP 4: User router imported", flush=True)

from src.interview.router import task_routes
print("STEP 5: Interview router imported", flush=True)

from src.question.router import ques_routes
print("STEP 6: Question router imported", flush=True)

from src.answer.router import ans_routes
print("STEP 7: Answer router imported", flush=True)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://frontend-system-design-interviewer.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(ques_routes)
app.include_router(task_routes)
app.include_router(user_routes)
app.include_router(ans_routes)

print("STEP 8: Application ready", flush=True)