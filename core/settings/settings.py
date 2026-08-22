from functools import lru_cache
from typing import Literal

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = 'FastAPI Template'
    APP_ENV: Literal['development', 'test', 'production'] = 'development'
    DEBUG: bool = False
    LOG_LEVEL: Literal['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'] = 'INFO'
    API_PREFIX: str = '/api/v1'

    DATABASE_URL: str = Field(
        default='postgresql+asyncpg://postgres:postgres@localhost:5432/app'
    )
    DATABASE_ECHO: bool = False

    SECRET_KEY: SecretStr = Field(min_length=32)
    JWT_SECRET_KEY: SecretStr = Field(min_length=32)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=30, ge=1, le=1440)
    ADMIN_ENABLED: bool = True
    ADMIN_USERNAME: str = Field(min_length=1)
    ADMIN_PASSWORD: SecretStr = Field(min_length=12)

    CORS_ORIGINS: list[str] = Field(default_factory=list)
    ALLOWED_HOSTS: list[str] = Field(default_factory=lambda: ['*'])

    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        env_ignore_empty=True,
        extra='ignore',
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()  # pyright: ignore[reportCallIssue]


settings = get_settings()
