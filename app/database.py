# app/database.py
import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlmodel import Session, SQLModel

load_dotenv()  # загружаем .env

DATABASE_URL = os.getenv("DATABASE_URL")

# Если DATABASE_URL не задан (например, при запуске тестов), используем SQLite
if not DATABASE_URL:
    DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(DATABASE_URL, echo=False, future=True)


def init_db():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session

