import os
from sqlalchemy import create_engine
from sqlmodel import Session, SQLModel

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError(
        "DATABASE_URL не задан. Переменная должна быть передана через environment "
        "(например, в docker-compose.yml), а не через .env файл."
    )


if DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = "postgresql+psycopg2" + DATABASE_URL[len("postgresql"):]
elif not DATABASE_URL.startswith("postgresql+psycopg2://"):
    raise ValueError(f"Неподдерживаемый формат DATABASE_URL: {DATABASE_URL}")

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









