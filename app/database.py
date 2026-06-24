import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel, create_engine as sqlmodel_create_engine

DATABASE_URL = os.getenv("DATABASE_URL")

engine = sqlmodel_create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()

def init_db():
    SQLModel.metadata.create_all(engine)
