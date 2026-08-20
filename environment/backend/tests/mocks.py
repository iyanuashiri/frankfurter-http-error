from tests.conftest import client, db


async def fake_convert(self, base_currency: str, target_currency: str):
    return {'amount': 1.0, 'base': 'USD', 'date': '2026-08-14', 'rates': {'CAD': 1.3875}}


async def fake_window(*args, **kwargs):
    class Window:
        remaining = 0
    return Window()    


async def fake_get_currencies(self):
    return {
        "USD": "US Dollar",
        "EUR": "Euro",
    }


async def fake_historical(self, date: str, base_currency: str, target_currency: str):
    return {
        "base_currency": base_currency,
        "date": date,
        "rates": {target_currency: 0.85},
        "credits": 9
    }


async def fake_historical_not_found(self, date, base_currency, target_currency):
    return None

# def create_user(client):
#     response = client.post(
#         "/api/v1/users/",
#         json={
#             "username": "john",
#             "password": "password123",
#         },
#     )
#     return response.json()


def create_user(client, username="james"):
    response = client.post(
        "/api/v1/users/",
        json={
            "username": username,
            "password": "password123",
        },
    )
    return response.json()