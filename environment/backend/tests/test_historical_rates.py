from app.services.currency_service import Currency
from app.crud.users import get_by_api_key
from app.api.routes.currencies import rate_limiter
from tests.mocks import create_user, fake_historical, fake_historical_not_found, fake_window
from tests.conftest import client, db
from tests.database import TestingSessionLocal


def test_historical_rates(client, monkeypatch):
    monkeypatch.setattr(Currency, "historical", fake_historical)

    user = create_user(client)

    response = client.get(
        "/api/v1/currencies/historical-rates/2026-01-01"
        "?base_currency=USD&target_currency=EUR",
        headers={
            "X-API-Key": user["api_key"]
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["base_currency"] == "USD"
    assert data["date"] == "2026-01-01"
    assert "rates" in data
    assert data["credits"] == 9


def test_historical_rates_not_enough_credits(client, monkeypatch):
    monkeypatch.setattr(Currency, "historical", fake_historical)

    user = create_user(client)

    db = TestingSessionLocal()
    db_user = get_by_api_key(db, user["api_key"])
    db_user.credits = 0
    db.commit()
    db.close()

    response = client.get(
        "/api/v1/currencies/historical-rates/2026-01-01",
        headers={
            "X-API-Key": user["api_key"]
        },
    )

    assert response.status_code == 403
    assert response.json()["detail"] == "Not enough credits"    


def test_historical_rates_not_found(client, monkeypatch):
    monkeypatch.setattr(
        Currency,
        "historical",
        fake_historical_not_found
    )

    user = create_user(client)

    response = client.get(
        "/api/v1/currencies/historical-rates/2026-01-01",
        headers={
            "X-API-Key": user["api_key"]
        },
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Historical currency rates not found"    


def test_historical_rates_rate_limit_exceeded(client, monkeypatch):
    monkeypatch.setattr(Currency, "historical", fake_historical)

    user = create_user(client)

    monkeypatch.setattr(rate_limiter, "get_window_stats", fake_window)

    response = client.get(
               "/api/v1/currencies/historical-rates/2026-01-01",
               headers={
                   "X-API-Key": user["api_key"]
               },
           )
   
    assert response.status_code == 429
    assert response.json()["detail"] == "Rate limit exceeded"    