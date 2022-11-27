from fastapi.testclient import TestClient

from .main import app

client = TestClient(app)


def test_create():
    response = client.post("/games")
    assert response.status_code == 201


def test_get():
    response = client.get("/games/08e5bbc9-050e-432d-b7e7-48ceec926e24")
    assert response.status_code == 200
