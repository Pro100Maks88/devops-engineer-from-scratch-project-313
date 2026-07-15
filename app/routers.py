import json

from fastapi import APIRouter, HTTPException, Query, Request, Response, status

from app.models import LinkCreate, LinkUpdate
from app.services import (
    create_link,
    delete_link,
    get_link_by_id,
    list_links,
    update_link,
)

router = APIRouter()


def build_short_url(request: Request | None, short_name: str) -> str:
    if request:
        base = f"{request.url.scheme}://{request.url.netloc}"
        return f"{base}/r/{short_name}"
    return f"http://localhost:8080/r/{short_name}"


@router.get("/ping")
def ping():
    return "pong"


@router.post("/api/links", status_code=status.HTTP_201_CREATED)
def api_create_link(
    link_in: LinkCreate,
    request: Request,
):
    data = create_link(link_in)
    data["short_url"] = build_short_url(request, data["short_name"])
    return data


@router.get("/api/links")
def api_list_links(
    request: Request,
    response: Response,
    range_param: str | None = Query(default=None, alias="range"),
):
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

        except json.JSONDecodeError:
            raise HTTPException(status_code=400, detail="Invalid range parameter")
        except ValueError as e:
            msg = str(e)
            if "2 elements" in msg:
                raise HTTPException(status_code=400, detail="Invalid range format")
            else:
                raise HTTPException(status_code=400, detail="Invalid range parameter")

    items = list_links(start, end, response)

    result = []
    for item in items:
        item["short_url"] = build_short_url(request, item["short_name"])
        result.append(item)

    return result


@router.get("/api/links/{link_id}")
def api_get_link(
    link_id: int,
    request: Request,
):
    data = get_link_by_id(link_id)
    data["short_url"] = build_short_url(request, data["short_name"])
    return data


@router.put("/api/links/{link_id}")
def api_update_link(
    link_id: int,
    link_in: LinkUpdate,
    request: Request,
):
    data = update_link(link_id, link_in)
    data["short_url"] = build_short_url(request, data["short_name"])
    return data


@router.delete("/api/links/{link_id}", status_code=status.HTTP_204_NO_CONTENT)
def api_delete_link(link_id: int):
    delete_link(link_id)
    return None
