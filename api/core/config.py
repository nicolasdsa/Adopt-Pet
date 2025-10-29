# api/core/config.py
from functools import lru_cache
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    app_name: str = Field("Adopt Pet API", alias="APP_NAME")
    database_url: str = Field(
        "sqlite:///./app.db", alias="DATABASE_URL", description="SQLAlchemy database URL"
    )
    debug: bool = Field(False, alias="DEBUG")

    # Pydantic v2 style
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

@lru_cache
def get_settings() -> Settings:
    return Settings()
