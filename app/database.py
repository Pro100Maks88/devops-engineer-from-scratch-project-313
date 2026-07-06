import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlmodel import Session, SQLModel

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError(
        "DATABASE_URL не задан. Для PostgreSQL укажите строку подключения в .env, "
        "например: postgresql+psycopg2://user:password@db:5432/mydb"
    )

engine = create_engine(
    DATABASE_URL,
    echo=False,
    future=True,
)

def init_db():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session






