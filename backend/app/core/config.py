"""
Application configuration loaded from environment variables.
All secrets come from .env — never hardcoded.
"""
from functools import lru_cache
from typing import Literal

from pydantic import AnyUrl, Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # App
    app_name: str = "Credwise API"
    app_version: str = "1.0.0"
    environment: Literal["development", "staging", "production"] = "development"
    debug: bool = False

    # Server
    host: str = "0.0.0.0"
    port: int = 8000
    allowed_origins: list[str] = Field(
        default=["http://localhost:5173", "http://localhost:3000"]
    )

    # Database
    database_url: str  # asyncpg DSN: postgresql+asyncpg://...
    db_min_size: int = 5
    db_max_size: int = 20
    db_max_inactive_conn_lifetime: float = 300.0

    # JWT
    jwt_secret_key: str
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7

    # Security
    bcrypt_rounds: int = 12

    # Rate limiting
    rate_limit_requests: int = 100
    rate_limit_window_seconds: int = 60

    @field_validator("allowed_origins", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v: str | list[str]) -> list[str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",") if i.strip()]
        if isinstance(v, list):
            return v
        import json
        return json.loads(v)

    @field_validator("database_url")
    @classmethod
    def database_url_must_be_asyncpg(cls, v: str) -> str:
        if "postgresql" not in v and "postgres" not in v:
            raise ValueError("DATABASE_URL must be a PostgreSQL connection string")
        # Normalise to asyncpg driver scheme
        v = v.replace("postgresql://", "postgresql+asyncpg://", 1)
        v = v.replace("postgres://", "postgresql+asyncpg://", 1)
        return v

    @property
    def is_production(self) -> bool:
        return self.environment == "production"

    @property
    def asyncpg_dsn(self) -> str:
        """Raw asyncpg DSN (no driver prefix) for asyncpg.create_pool()."""
        return (
            self.database_url
            .replace("postgresql+asyncpg://", "postgresql://")
        )


@lru_cache
def get_settings() -> Settings:
    return Settings()  # type: ignore[call-arg]
