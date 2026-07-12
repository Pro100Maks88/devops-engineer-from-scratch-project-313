import json
from typing import Any

from fastapi import HTTPException, Response
from sqlmodel import func, select

from app.database import get_session
from app.models import Link, LinkCreate, LinkUpdate


def _to_response_dict(link: Link) -> dict[str, Any]:
    
    return {
        "id": link.id,
        "original_url": link.original_url,
        "short_name": link.short_name,
        "created_at": link.created_at.isoformat(),
        "short_url": f"/r/{link.short_name}",
    }


def create_link(link_in: LinkCreate) -> dict[str, Any]:
    
    with get_session() as session:
        
        existing = session.exec(
            select(Link).where(Link.short_name == link_in.short_name)
        ).first()

        if existing:
            raise HTTPException(status_code=409, detail="Short name already exists")

        link = Link(**link_in.model_dump())
        session.add(link)
        session.commit()
        session.refresh(link)

        return _to_response_dict(link)


def list_links(range_param: str | None, response: Response) -> list[dict[str, Any]]:
    
    start = 0
    end = 20

    if range_param is not None:
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
            raise HTTPException(status_code=400, detail="Invalid range parameter")
        except ValueError as e:
            msg = str(e)
            if "2 elements" in msg:
                raise HTTPException(status_code=400, detail="Invalid range format")
            else:
                raise HTTPException(status_code=400, detail="Invalid range parameter")

    limit = end - start
    if limit <= 0:
        limit = 1

    with get_session() as session:
        total_count = session.exec(select(func.count(Link.id))).one()
        statement = select(Link).offset(start).limit(limit)
        links = session.exec(statement).all()

    response.headers["Content-Range"] = f"links {start}-{end}/{total_count}"
    return [_to_response_dict(link) for link in links]


def get_link_by_id(link_id: int) -> dict[str, Any]:
    
    with get_session() as session:
        link = session.exec(select(Link).where(Link.id == link_id)).first()
        if not link:
            raise HTTPException(status_code=404, detail="Link not found")
        return _to_response_dict(link)


def update_link(link_id: int, link_in: LinkUpdate) -> dict[str, Any]:
    
    with get_session() as session:
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

        return _to_response_dict(link)


def delete_link(link_id: int) -> None:
    
    with get_session() as session:
        link = session.exec(select(Link).where(Link.id == link_id)).first()
        if not link:
            raise HTTPException(status_code=404, detail="Link not found")

        session.delete(link)
        session.commit()
    






