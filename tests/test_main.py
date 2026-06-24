import pytest
from fastapi.testclient import TestClient
from main import app
from app.database import init_db, engine
from app.models import Link

@pytest.fixture(autouse=True)
def setup_db():
    init_db()
    yield
    with engine.connect() as conn:
        conn.execute("TRUNCATE TABLE links RESTART IDENTITY CASCADE;")
        conn.commit()

client = TestClient(app)

def test_create_link():
    res = client.post("/api/links", json={"original_url": "https://example.com", "short_name": "exmpl"})
    assert res.status_code == 201
    data = res.json()
    assert data["original_url"] == "https://example.com"
    assert data["short_name"] == "exmpl"
    assert "short_url" in data

def test_list_links():
    client.post("/api/links", json={"original_url": "https://a.com", "short_name": "a"})
    client.post("/api/links", json={"original_url": "https://b.com", "short_name": "b"})
    res = client.get("/api/links")
    assert res.status_code == 200
    assert len(res.json()) == 2

def test_get_link_by_id():
    res_create = client.post("/api/links", json={"original_url": "https://c.com", "short_name": "c"})
    link_id = res_create.json()["id"]
    res = client.get(f"/api/links/{link_id}")
    assert res.status_code == 200
    assert res.json()["id"] == link_id

def test_update_link():
    res_create = client.post("/api/links", json={"original_url": "https://d.com", "short_name": "d"})
    link_id = res_create.json()["id"]
    res = client.put(f"/api/links/{link_id}", json={"original_url": "https://d-new.com", "short_name": "d-new"})
    assert res.status_code == 200
    assert res.json()["original_url"] == "https://d-new.com"

def test_delete_link():
    res_create = client.post("/api/links", json={"original_url": "https://e.com", "short_name": "e"})
    link_id = res_create.json()["id"]
    res = client.delete(f"/api/links/{link_id}")
    assert res.status_code == 204
    res_get = client.get(f"/api/links/{link_id}")
    assert res_get.status_code == 404

def test_unique_short_name():
    client.post("/api/links", json={"original_url": "https://x.com", "short_name": "uniq"})
    res = client.post("/api/links", json={"original_url": "https://y.com", "short_name": "uniq"})
    assert res.status_code == 409

