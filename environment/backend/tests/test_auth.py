from tests.conftest import client


def test_missing_api_key(client):

    response = client.get("/api/v1/currencies/")

    assert response.status_code == 422


def test_invalid_api_key(client):
    response = client.get(
        "/api/v1/currencies/",
        headers={
            "X-API-Key": "invalid-key"
        },
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid API Key or User not found"    