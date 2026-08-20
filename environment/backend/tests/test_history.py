
from urllib import response

from app.api.routes.currencies import rate_limiter  
from app.services.currency_service import Currency
from tests.mocks import fake_window, create_user, fake_convert 
from tests.conftest import client, db


def test_get_history(client, monkeypatch):
    user = create_user(client)
    monkeypatch.setattr(Currency, "convert", fake_convert)
    response1 =client.get(
        "/api/v1/currencies/conversions?base_currency=USD&target_currency=CAD&amount=100",
        headers={
            "X-API-Key": user["api_key"]
            },
        )
    assert response1.status_code == 200
    response2 = client.get("/api/v1/currencies/history/", headers={"X-API-Key": user["api_key"]})

    assert response2.status_code == 200
    data = response2.json()
    assert len(data) == 1
    assert data[0]["base_currency"] == "USD"
    assert data[0]["target_currency"] == "CAD"
    assert data[0]["amount"] == 100   
   

def test_history_empty(client):
    user = create_user(client)

    response = client.get(
        "/api/v1/currencies/history",
        headers={
            "X-API-Key": user["api_key"]
        },
    )

    assert response.status_code == 200
    assert response.json() == []


def test_history_missing_api_key(client):
    response = client.get("/api/v1/currencies/history")

    assert response.status_code == 422    


def test_history_only_returns_current_users_conversions(client, monkeypatch):
    monkeypatch.setattr(Currency, "convert", fake_convert)

    user1 = create_user(client)
    user2 = create_user(client, username="alice")

    response1 = client.get(
        "/api/v1/currencies/conversions"
        "?base_currency=USD&target_currency=CAD&amount=100",
        headers={"X-API-Key": user1["api_key"]},
    )

    assert response1.status_code == 200

    response2 = client.get(
        "/api/v1/currencies/history",
        headers={"X-API-Key": user2["api_key"]},
    )

    assert response2.status_code == 200
    assert response2.json() == []    