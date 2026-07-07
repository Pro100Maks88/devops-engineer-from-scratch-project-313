import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlmodel import Session, SQLModel

if os.path.exists(".env"):
    load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")


if not DATABASE_URL:
    raise RuntimeError(
        "DATABASE_URL не задан. Создай .env файл или проверь окружение."
    )

if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql+psycopg://")

engine = create_engine(DATABASE_URL, echo=False, future=True)

def init_db():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session










