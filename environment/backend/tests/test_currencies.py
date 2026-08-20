from app.services.currency_service import Currency
from app.crud.users import get_by_api_key
from app.api.routes.currencies import rate_limiter
from tests.database import TestingSessionLocal
from tests.conftest import client, db
from tests.mocks import fake_window, create_user, fake_get_currencies


def test_get_currencies(client, monkeypatch):
    monkeypatch.setattr(Currency, "get_currencies", fake_get_currencies)
    user = create_user(client)

    response = client.get(
        "/api/v1/currencies/",
        headers={
            "X-API-Key": user["api_key"]
        },
    )

    assert response.status_code == 200    
    data = response.json()

    assert "currencies" in data
    assert data["credits"] == 9


def test_get_currencies_not_enough_credits(client, monkeypatch):
    monkeypatch.setattr(Currency, "get_currencies", fake_get_currencies)
    user = create_user(client)

    db = TestingSessionLocal()
    db_user = get_by_api_key(db, user["api_key"])
    db_user.credits = 0
    db.commit()
    db.close()

    response = client.get(
        "/api/v1/currencies/",
        headers={
            "X-API-Key": user["api_key"]
        },
    )

    assert response.status_code == 403
    assert response.json()["detail"] == "Not enough credits"    


def test_get_currencies_rate_limit_exceeded(client, monkeypatch):
    monkeypatch.setattr(Currency, "get_currencies", fake_get_currencies)
    user = create_user(client)

    monkeypatch.setattr(rate_limiter, "get_window_stats", fake_window)
    response = client.get(
                "/api/v1/currencies/",
                headers={
                    "X-API-Key": user["api_key"]
                },
            )
    
    # Simulate the user hitting the rate limit
   
    assert response.status_code == 429
    assert response.json()["detail"] == "Rate limit exceeded"    


# def test_get_currencies_rate_limit_exceeded(client, monkeypatch):
#     monkeypatch.setattr(Currency, "get_currencies", fake_get_currencies)
#     user = create_user(client)
    
#     # Simulate the user hitting the rate limit
#     for i in range(9):
#         response = client.get(
#             "/api/v1/currencies/",
#             headers={
#                 "X-API-Key": user["api_key"]
#             },
#         )
#         print(i + 1, response.status_code)
#         assert response.status_code == 200

#     # The next request should hit the rate limit
#     response = client.get(
#         "/api/v1/currencies/",
#         headers={
#             "X-API-Key": user["api_key"]
#         },
#     )

#     assert response.status_code == 429
#     assert response.json()["detail"] == "Rate limit exceeded"    


def test_get_currencies_invalid_api_key(client):
    response = client.get(
        "/api/v1/currencies/",
        headers={
            "X-API-Key": "invalid_api_key"
        },
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid API Key or User not found"    


