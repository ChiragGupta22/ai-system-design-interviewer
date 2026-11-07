from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from src.User.settings import settings

Base = declarative_base()

engine = create_engine(
    url=settings.DATABASE_URL,
    pool_pre_ping=True
)

LocalSession = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False
)

def get_db():
    session = LocalSession()
    try:
        yield session
    finally:
        session.close()