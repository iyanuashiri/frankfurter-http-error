from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        populate_by_name=True,
        env_file=".env",
        extra="ignore",
    )

    database_url: str = Field(default="sqlite:///./currency.db", alias="DATABASE_URL")
    frankfurter_host: str = Field(default="api.frankfurter.dev", alias="FRANKFURTER_HOST")

    @property
    def DATABASE_URL(self) -> str:
        return self.database_url

    @property
    def FRANKFURTER_HOST(self) -> str:
        return self.frankfurter_host


settings = Settings()
