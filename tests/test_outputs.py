"""
Use this file to define pytest tests that verify the outputs of the task.

This file will be copied to /tests/test_outputs.py and run by the /tests/test.sh file
from the working directory.
"""


from fastapi import HTTPException
from fastapi.testclient import TestClient

from app.main import app
from frankfurter.rest_adapter import RestAdapter

client = TestClient(app)


def fake_get(self, url):
    raise HTTPException(
        status_code=503,
        detail="Could not connect to external currency service",
    )


def test_external_api_returns_503(monkeypatch):
    """
    The API should preserve upstream HTTP errors instead of
    returning an internal server error.
    """

    monkeypatch.setattr(RestAdapter, "get", fake_get)

    response = client.post(
        "/api/v1/users/",
        json={
            "username": "tester",
            "password": "password123",
        },
    )

    assert response.status_code == 201

    api_key = response.json()["api_key"]

    response = client.get(
        "/api/v1/currencies/",
        headers={
            "X-API-Key": api_key,
        },
    )

    assert response.status_code == 503

    body = response.json()

    assert "detail" in body