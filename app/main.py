import os
import uvicorn
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from contextlib import asynccontextmanager

from app.database import engine, get_session, init_db
from app.models import Link, LinkCreate, LinkRead

BASE_URL = os.getenv("BASE_URL", "http://localhost:8080")

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()  # Создаём таблицы при старте
    yield

app = FastAPI(lifespan=lifespan)

@app.post("/api/links", response_model=LinkRead, status_code=status.HTTP_201_CREATED)
def create_link(link_in: LinkCreate, session: Session = Depends(get_session)):
    existing = session.query(Link).filter(Link.short_name == link_in.short_name).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Short name already exists",
        )
    link = Link(**link_in.dict())
    session.add(link)
    session.commit()
    session.refresh(link)
    return LinkRead.from_orm(link, BASE_URL)

@app.get("/api/links", response_model=list[LinkRead])
def list_links(session: Session = Depends(get_session)):
    links = session.query(Link).all()
    return [LinkRead.from_orm(l, BASE_URL) for l in links]

@app.get("/api/links/{link_id}", response_model=LinkRead)
def get_link(link_id: int, session: Session = Depends(get_session)):
    link = session.query(Link).filter(Link.id == link_id).first()
    if not link:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Link not found")
    return LinkRead.from_orm(link, BASE_URL)

@app.put("/api/links/{link_id}", response_model=LinkRead)
def update_link(link_id: int, link_in: LinkCreate, session: Session = Depends(get_session)):
    link = session.query(Link).filter(Link.id == link_id).first()
    if not link:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Link not found")

    if link.short_name != link_in.short_name:
        existing = session.query(Link).filter(Link.short_name == link_in.short_name).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Short name already exists",
            )

    link.original_url = link_in.original_url
    link.short_name = link_in.short_name
    session.commit()
    session.refresh(link)
    return LinkRead.from_orm(link, BASE_URL)

@app.delete("/api/links/{link_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_link(link_id: int, session: Session = Depends(get_session)):
    link = session.query(Link).filter(Link.id == link_id).first()
    if not link:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Link not found")
    session.delete(link)
    session.commit()