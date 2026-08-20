from app.api.routes.currencies import rate_limiter
from app.services.currency_service import Currency
from app.crud.users import get_by_api_key

from tests.database import TestingSessionLocal
from tests.conftest import client, db
from tests.mocks import fake_convert, fake_window, create_user




def test_convert_currency(client, monkeypatch):
    monkeypatch.setattr(Currency, "convert", fake_convert)
    user = create_user(client)

    response = client.get(
        "/api/v1/currencies/conversions?base_currency=USD&target_currency=CAD&amount=100",
        headers={
            "X-API-Key": user["api_key"]
        },
    )

    assert response.status_code == 200
    data = response.json()

    assert data["base_currency"] == "USD"
    assert data["target_currency"] == "CAD"
    assert data["amount"] == 100
    assert data["converted_amount"] == 138.75


def test_convert_currency_invalid_api(client, monkeypatch):
    monkeypatch.setattr(Currency, "convert", fake_convert)
    user = create_user(client)

    response = client.get(
        "/api/v1/currencies/conversions?base_currency=USD&target_currency=CAD&amount=100",
        headers={
            "X-API-Key": "invalid_api_key"
        },
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid API Key or User not found"


def test_convert_currency_not_enough_credits(client, monkeypatch):
    monkeypatch.setattr(Currency, "convert", fake_convert)
    user = create_user(client)

    db = TestingSessionLocal()
    db_user = get_by_api_key(db, user["api_key"])
    db_user.credits = 0
    db.commit()
    db.close()

    response = client.get(
        "/api/v1/currencies/conversions?base_currency=USD&target_currency=CAD&amount=100",
        headers={
            "X-API-Key": user["api_key"]
        },
    )

    assert response.status_code == 403
    assert response.json()["detail"] == "Not enough credits"


def test_convert_currency_rate_limit_exceeded(client, monkeypatch):
    monkeypatch.setattr(Currency, "convert", fake_convert)
    user = create_user(client)

    # db = TestingSessionLocal()
    # db_user = get_by_api_key(db, user["api_key"])
    # db_user.credits = 100
    # db.commit()
    # db.close()

    monkeypatch.setattr(rate_limiter, "get_window_stats", fake_window)
    response = client.get(
        "/api/v1/currencies/conversions?base_currency=USD&target_currency=CAD&amount=100",
        headers={
            "X-API-Key": user["api_key"]
        },
    )
    assert response.status_code == 429
    assert response.json()["detail"] == "Rate limit exceeded"

    # Simulate the user hitting the rate limit
    # for i in range(10):
    #     response = client.get(
    #         "/api/v1/currencies/conversions?base_currency=USD&target_currency=CAD&amount=100",
    #         headers={
    #             "X-API-Key": user["api_key"]
    #         },
    #     )
    #     print(i + 1, response.status_code)
    #     assert response.status_code == 200

    # The next request should hit the rate limit
    # response = client.get(
    #     "/api/v1/currencies/conversions?base_currency=USD&target_currency=CAD&amount=100",
    #     headers={
    #         "X-API-Key": user["api_key"]
    #     },
    # )

    # assert response.status_code == 429
    # assert response.json()["detail"] == "Rate limit exceeded"        