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
    client.post("/api/links", json={"original_url": "https://x.com", "short_name": "uniq"})
    res = client.post("/api/links", json={"original_url": "https://y.com", "short_name": "uniq"})
    assert res.status_code == 409
    assert res.json().get("detail") == "Short name already exists"
