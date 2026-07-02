import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlmodel import Session, SQLModel

from app import database
from app.main import app

test_engine = create_engine("sqlite:///./test.db", echo=False, future=True)

@pytest.fixture(scope="function")
def session():
    SQLModel.metadata.create_all(test_engine)
    with Session(test_engine) as session:
        yield session
    SQLModel.metadata.drop_all(test_engine)

@pytest.fixture(scope="function")
def client(session, monkeypatch):
    original_engine = database.engine
    database.engine = test_engine
    client = TestClient(app)
    yield client
    database.engine = original_engine


def test_create_link(client):
    res = client.post(
        "/api/links",
        json={"original_url": "https://example.com", "short_name": "exmpl"}
    )
    assert res.status_code == 201
    data = res.json()
    assert data["original_url"] == "https://example.com"
    assert data["short_name"] == "exmpl"
    assert "id" in data


def test_list_links(client):
    client.post("/api/links", json={"original_url": "https://a.com", "short_name": "a"})
    client.post("/api/links", json={"original_url": "https://b.com", "short_name": "b"})
    res = client.get("/api/links")
    assert res.status_code == 200
    assert len(res.json()) == 2


def test_get_link_by_id_success(client):
    res_create = client.post(
        "/api/links",
        json={"original_url": "https://c.com", "short_name": "c"}
    )
    assert res_create.status_code == 201
    link_id = res_create.json()["id"]

    res = client.get(f"/api/links/{link_id}")
    assert res.status_code == 200
    assert res.json()["id"] == link_id


def test_get_link_by_id_not_found(client):
    res = client.get("/api/links/99999")
    assert res.status_code == 404
    assert res.json().get("detail") == "Link not found"


def test_update_link(client):
    res_create = client.post(
        "/api/links",
        json={"original_url": "https://d.com", "short_name": "d"}
    )
    link_id = res_create.json()["id"]

    res = client.put(
        f"/api/links/{link_id}",
        json={"original_url": "https://d-new.com", "short_name": "d-new"}
    )
    assert res.status_code == 200
    assert res.json()["original_url"] == "https://d-new.com"


def test_delete_link(client):
    res_create = client.post(
        "/api/links",
        json={"original_url": "https://e.com", "short_name": "e"}
    )
    link_id = res_create.json()["id"]

    res = client.delete(f"/api/links/{link_id}")
    assert res.status_code == 204

    res_get = client.get(f"/api/links/{link_id}")
    assert res_get.status_code == 404

def test_unique_short_name_conflict(client):
    payload = {"original_url": "https://x.com", "short_name": "uniq"}
    client.post("/api/links", json=payload)

    payload_conflict = {"original_url": "https://y.com", "short_name": "uniq"}
    res = client.post("/api/links", json=payload_conflict)

    assert res.status_code == 409
    assert res.json().get("detail") == "Short name already exists"



# --- Тесты пагинации ---

def test_list_links_default_pagination(client):
    for i in range(25):
        client.post(
            "/api/links",
            json={"original_url": f"https://{i}.com", "short_name": f"short{i}"}
        )

    res = client.get("/api/links")
    assert res.status_code == 200
    data = res.json()

    assert len(data) == 20

    assert "Content-Range" in res.headers
    header = res.headers["Content-Range"]
    assert header.startswith("links 0-20/")
    total = int(header.split("/")[1])
    assert total == 25


def test_list_links_with_range_explicit(client):
    for i in range(15):
        client.post(
            "/api/links",
            json={"original_url": f"https://{i}.com", "short_name": f"short{i}"}
        )

    res = client.get("/api/links?range=[0,10]")
    assert res.status_code == 200
    data = res.json()

    assert len(data) == 10

    header = res.headers["Content-Range"]
    assert header == "links 0-10/15"


def test_list_links_offset_range(client):
    for i in range(12):
        client.post(
            "/api/links",
            json={"original_url": f"https://{i}.com", "short_name": f"short{i}"}
        )

    res = client.get("/api/links?range=[5,10]")
    assert res.status_code == 200
    data = res.json()

    assert len(data) == 5
    assert data[0]["id"] == 6

    header = res.headers["Content-Range"]
    assert header == "links 5-10/12"


def test_list_links_invalid_range_not_json(client):
    res = client.get("/api/links?range=not_json")
    assert res.status_code == 400
    assert "Invalid range parameter" in res.json().get("detail", "")


def test_list_links_bad_format_range(client):
    res = client.get("/api/links?range=[1,2,3]")
    assert res.status_code == 400
    assert "Invalid range format" in res.json().get("detail", "")

test_engine = create_engine(
    "sqlite:///./test.db",
    echo=False,
    future=True,
    connect_args={"check_same_thread": False} 
)

