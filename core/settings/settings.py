from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DB_NAME: str = Field(default=...)
    DB_USER: str = Field(default=...)
    DB_PASSWORD: str = Field(default=...)

    model_config = SettingsConfigDict(env_file='.env')


settings = Settings()
