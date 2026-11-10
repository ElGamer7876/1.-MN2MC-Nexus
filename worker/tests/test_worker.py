"""Basic offline API tests. Run pip install httpx pytest to use."""
import os
from fastapi.testclient import TestClient
from app.main import app

def test_regions_without_database(monkeypatch):
    monkeypatch.delenv("MYSQL_HOST", raising=False)
    with TestClient(app) as client:
        response = client.get("/regions")
        assert response.status_code == 200
        assert "usz" in response.json()["candidates"]

def test_admin_requires_token(monkeypatch):
    monkeypatch.delenv("NEXUS_API_TOKEN", raising=False)
    with TestClient(app) as client:
        response = client.put("/rooms/usz/test", json={
            "account_alias": "test", "players": 1, "capacity": 40, "status": "open"
        })
        assert response.status_code == 503

def test_room_reads_fail_closed_without_database(monkeypatch):
    monkeypatch.delenv("MYSQL_HOST", raising=False)
    with TestClient(app) as client:
        assert client.get("/rooms").status_code == 503
