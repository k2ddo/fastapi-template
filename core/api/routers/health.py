from fastapi import APIRouter, HTTPException, status
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from ...orm.database import engine

router = APIRouter(prefix='/health', tags=['health'])


@router.get('/live', include_in_schema=False)
async def liveness() -> dict[str, str]:
    return {'status': 'ok'}


@router.get('/ready', include_in_schema=False)
async def readiness() -> dict[str, str]:
    try:
        async with engine.connect() as connection:
            await connection.execute(text('SELECT 1'))
    except SQLAlchemyError as error:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail='Database is unavailable',
        ) from error
    return {'status': 'ok'}
