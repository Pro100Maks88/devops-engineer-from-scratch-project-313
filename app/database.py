import os
from sqlalchemy import create_engine
from sqlmodel import Session, SQLModel

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError(
        "DATABASE_URL не задан. Переменная должна быть передана через environment "
        "(например, в docker-compose.yml), а не через .env файл."
    )

engine = create_engine(
    DATABASE_URL,
    echo=True,
    future=True,
)

def init_db():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session








