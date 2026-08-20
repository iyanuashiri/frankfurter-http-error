import pytest

from app.core.config import Settings


def test_settings_accepts_frankfurter_host(monkeypatch):
    monkeypatch.setenv("FRANKFURTER_HOST", "api.frankfurter.dev")

    settings = Settings()

    assert settings.frankfurter_host == "api.frankfurter.dev"
    assert settings.FRANKFURTER_HOST == "api.frankfurter.dev"
    assert settings.DATABASE_URL == "sqlite:///./currency.db"
