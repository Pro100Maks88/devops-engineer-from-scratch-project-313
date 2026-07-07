from contextlib import contextmanager

from fastapi import Depends, FastAPI, HTTPException, Query, Response, status
from sqlalchemy import func
from sqlmodel import Session, select

from app import database
from app.models import Link, LinkCreate, LinkUpdate


@contextmanager
def get_session():
    
    session = database.SessionLocal()
    try:
        yield session
    finally:
        session.close()


def get_session_dep() -> Session:
   
    return next(get_session())


@contextmanager
def lifespan(app: FastAPI):
   
    database.init_db()
    yield


app = FastAPI(
    title="Short Link Service",
    version="1.0.0",
    lifespan=lifespan,
)


@app.get("/ping")
def ping():

    return {"data": "pong"}


@app.post("/api/links", response_model=Link, status_code=status.HTTP_201_CREATED)
def create_link(
    link_in: LinkCreate,
    session: Session = Depends(get_session_dep),
):
    existing = session.exec(
        select(Link).where(Link.short_name == link_in.short_name)
    ).first()

    if existing:
        raise HTTPException(status_code=409, detail="Short name already exists")

    link = Link(**link_in.model_dump())
    session.add(link)
    session.commit()
    session.refresh(link)
    return link


@app.get("/api/links")
def list_links(
    response: Response,
    range_param: str | None = Query(default=None, alias="range"),
    session: Session = Depends(get_session_dep),
):
    start = 0
    end = 20

    if range_param is not None:
        import json
        try:
            parsed = json.loads(range_param)

            if not isinstance(parsed, list):
                raise ValueError("Range must be a list")
            if len(parsed) != 2:
                raise ValueError("Range must have exactly 2 elements")

            start, end = parsed

            if start < 0 or end < 0:
                raise ValueError("Start and end must be non-negative")
            if end <= start:
                raise ValueError("End must be greater than start")

        except json.JSONDecodeError:
            raise HTTPException(
                status_code=400,
                detail="Invalid range parameter",
            )
        except ValueError as e:
            msg = str(e)
            if "2 elements" in msg:
                raise HTTPException(
                    status_code=400,
                    detail="Invalid range format",
                )
            else:
                raise HTTPException(
                    status_code=400,
                    detail="Invalid range parameter",
                )

    limit = end - start
    if limit <= 0:
        limit = 1

    total_count = session.exec(select(func.count(Link.id))).one()

    statement = select(Link).offset(start).limit(limit)
    links = session.exec(statement).all()

    response.headers["Content-Range"] = f"links {start}-{end}/{total_count}"

    return links


@app.get("/api/links/{link_id}")
def get_link(
    link_id: int,
    session: Session = Depends(get_session_dep),
):
    link = session.exec(select(Link).where(Link.id == link_id)).first()
    if not link:
        raise HTTPException(status_code=404, detail="Link not found")
    return link


@app.put("/api/links/{link_id}", response_model=Link)
def update_link(
    link_id: int,
    link_in: LinkUpdate,
    session: Session = Depends(get_session_dep),
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
def delete_link(
    link_id: int,
    session: Session = Depends(get_session_dep),
):
    link = session.exec(select(Link).where(Link.id == link_id)).first()
    if not link:
        raise HTTPException(status_code=404, detail="Link not found")

    session.delete(link)
    session.commit()
    return None


