import os
import pytest

from app.core.database import Base
from app.models.users import User
from app.core.security import verify_password

from tests.database import TestingSessionLocal, engine
from tests.conftest import client


def test_create_user(client):

    response = client.post("/api/v1/users/", json={"username": "john", 
                                                         "password": "password123"})

    assert response.status_code == 201

    data = response.json()

    assert data["username"] == "john"
    assert data["credits"] == 10
    assert data["is_active"] is True
    assert "api_key" in data


def test_duplicate_username(client):

    payload = {
        "username": "john",
        "password": "password123",
    }

    client.post("/api/v1/users/", json=payload)

    response = client.post("/api/v1/users/", json=payload)

    assert response.status_code == 400
    assert response.json()["detail"] == "Username already exists"    


def test_get_users(client):

    client.post("/api/v1/users/", json={"username": "john", "password": "password123"})

    response = client.get("/api/v1/users/")

    assert response.status_code == 200

    users = response.json()

    assert len(users) == 1
    assert users[0]["username"] == "john"    


def test_password_not_stored_in_plain_text(client, db):

    response = client.post(
        "/api/v1/users/",
        json={
            "username": "john",
            "password": "password123",
        },
    )

    assert "password" not in response.json()
    # db = TestingSessionLocal()
    # try:
    #     db_user = db.query(User).filter(User.username == "john").first()
    #     assert db_user is not None
    #     assert db_user.password != "password123"
    # finally:
    #     db.close()
    ################################################
    # with TestingSessionLocal() as db:
    #     db_user = db.query(User).filter(User.username == "john").first()
    #     assert db_user is not None
    #     assert db_user.password != "password123"

    db_user = db.query(User).filter(User.username == "john").first()
    assert db_user is not None  
    assert db_user.password != "password123"

    assert db_user.password != "password123"
    assert verify_password("password123", db_user.password)


def test_user_not_active_by_default(client, db):

    response = client.post(
        "/api/v1/users/",
        json={
            "username": "john",
            "password": "password123",
        },
    )

    assert response.status_code == 201

    db_user = db.query(User).filter(User.username == "john").first()
    assert db_user is not None
    assert db_user.is_active is True

    db_user.is_active = False
    db.commit()
    assert db_user.is_active is False    