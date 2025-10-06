from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).parent.parent

print(BASE_DIR)


class Settings(BaseSettings):
    DB_NAME: str = Field(default=...)
    DB_USER: str = Field(default=...)
    DB_PASSWORD: str = Field(default=...)

    SECRET_KEY: str = Field(default=...)

    model_config = SettingsConfigDict(env_file='.env')


settings = Settings()
