from fastapi import FastAPI
from src.db import Base, engine
from src.router import user_routes
Base.metadata.create_all(engine)

app = FastAPI()

app.include_router(user_routes)