from fastapi import FastAPI, HTTPException, Depends, status
from sqlmodel import Session, select
from typing import List

from .database import engine, get_session
from .models import Link, LinkCreate, LinkUpdate

app = FastAPI()


@app.get("/ping")
def ping():
    return "pong"


def _link_to_dict(link: Link) -> dict:
    """Вспомогательная функция: превращает Link в dict с обязательным short_url"""
    return {
        "id": link.id,
        "original_url": link.original_url,
        "short_name": link.short_name,
        "created_at": link.created_at.isoformat(),
        "short_url": f"/r/{link.short_name}",  
    }


@app.post("/api/links", status_code=status.HTTP_201_CREATED)
def create_link(link_in: LinkCreate, session: Session = Depends(get_session)):
    existing = session.exec(select(Link).where(Link.short_name == link_in.short_name)).first()
    if existing:
        raise HTTPException(status_code=409, detail="Short name already exists")

    link = Link(**link_in.model_dump())
    session.add(link)
    session.commit()
    session.refresh(link)

    return _link_to_dict(link)


@app.get("/api/links")
def list_links(session: Session = Depends(get_session)):
    links = session.exec(select(Link)).all()
    return [_link_to_dict(l) for l in links]


@app.get("/api/links/{link_id}")
def get_link(link_id: int, session: Session = Depends(get_session)):
    link = session.get(Link, link_id)
    if not link:
        raise HTTPException(status_code=404, detail="Link not found")
    return _link_to_dict(link)


@app.put("/api/links/{link_id}")
def update_link(link_id: int, link_in: LinkUpdate, session: Session = Depends(get_session)):
    link = session.get(Link, link_id)
    if not link:
        raise HTTPException(status_code=404, detail="Link not found")

    update_data = link_in.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(link, key, value)

    session.add(link)
    session.commit()
    session.refresh(link)

    return _link_to_dict(link)


@app.delete("/api/links/{link_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_link(link_id: int, session: Session = Depends(get_session)):
    link = session.get(Link, link_id)
    if not link:
        raise HTTPException(status_code=404, detail="Link not found")
    session.delete(link)
    session.commit()
    





