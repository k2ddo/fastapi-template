from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import DeclarativeBase

from ..settings import settings

database_url = f'postgresql+asyncpg://{settings.DB_USER}:{settings.DB_PASSWORD}@localhost:5432/{settings.DB_NAME}'
engine = create_async_engine(database_url, echo=True)


class Base(DeclarativeBase):
    pass
