from sqlalchemy import create_engine
from sqlmodel import Session, SQLModel

if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql+psycopg://")

engine = create_engine(DATABASE_URL, echo=False, future=True)

def init_db():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session










