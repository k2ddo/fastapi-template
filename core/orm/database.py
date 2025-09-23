from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import DeclarativeBase

database_url = 'sqlite+aiosqlite:///database.db'
engine = create_async_engine(database_url, echo=True)


class Base(DeclarativeBase):
    pass
