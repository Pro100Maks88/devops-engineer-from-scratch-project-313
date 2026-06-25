
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, select

from app import database
from app.models import Link, LinkCreate, LinkUpdate

app = FastAPI(title="Short Link Service", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_session() -> Session:
    with Session(database.engine) as session:
        yield session

@app.get("/ping")
def ping():
    return {"status": "ok"}

@app.post("/api/links", response_model=Link, status_code=status.HTTP_201_CREATED)
def create_link(link_in: LinkCreate, session: Session = Depends(get_session)):
    existing = session.exec(
        select(Link).where(Link.short_name == link_in.short_name)
    ).first()
    if existing:
        raise HTTPException(status_code=409, detail="Short name already exists")

    link = Link(**link_in.model_dump())
    session.add(link)
    session.commit()
    session.refresh(link)  # подтягивает id из БД
    return link

@app.get("/api/links")
def list_links(session: Session = Depends(get_session)):
    links = session.exec(select(Link)).all()
    return links

@app.get("/api/links/{link_id}")
def get_link(link_id: int, session: Session = Depends(get_session)):
    link = session.exec(select(Link).where(Link.id == link_id)).first()
    if not link:
        raise HTTPException(status_code=404, detail="Link not found")
    return link

@app.put("/api/links/{link_id}", response_model=Link)
def update_link(
    link_id: int,
    link_in: LinkUpdate,
    session: Session = Depends(get_session)
):
    link = session.exec(select(Link).where(Link.id == link_id)).first()
    if not link:
        raise HTTPException(status_code=404, detail="Link not found")

    if link_in.short_name is not None and link_in.short_name != link.short_name:
        existing = session.exec(
            select(Link).where(Link.short_name == link_in.short_name)
        ).first()
        if existing:
            raise HTTPException(status_code=409, detail="Short name already exists")

    for field, value in link_in.model_dump(exclude_unset=True).items():
        setattr(link, field, value)

    session.add(link)
    session.commit()
    session.refresh(link)
    return link

@app.delete("/api/links/{link_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_link(link_id: int, session: Session = Depends(get_session)):
    link = session.exec(select(Link).where(Link.id == link_id)).first()
    if not link:
        raise HTTPException(status_code=404, detail="Link not found")

    session.delete(link)
    session.commit()
    return None
