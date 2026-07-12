from fastapi import APIRouter, Query, Response, status

from app.models import LinkCreate, LinkUpdate
from app.services import (
    create_link,
    delete_link,
    get_link_by_id,
    list_links,
    update_link,
)

router = APIRouter()


@router.get("/ping")
def ping():
    return "pong"


@router.post("/api/links", status_code=status.HTTP_201_CREATED)
def api_create_link(link_in: LinkCreate):
    
    return create_link(link_in)


@router.get("/api/links")
def api_list_links(
    response: Response,
    range_param: str | None = Query(default=None, alias="range"),
):
    return list_links(range_param, response)


@router.get("/api/links/{link_id}")
def api_get_link(link_id: int):
    return get_link_by_id(link_id)


@router.put("/api/links/{link_id}")
def api_update_link(link_id: int, link_in: LinkUpdate):
    return update_link(link_id, link_in)


@router.delete("/api/links/{link_id}", status_code=status.HTTP_204_NO_CONTENT)
def api_delete_link(link_id: int):
    delete_link(link_id)
    return None



