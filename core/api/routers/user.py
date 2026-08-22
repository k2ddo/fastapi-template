from fastapi import APIRouter, HTTPException, Query, status
from pwdlib import PasswordHash
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from ...orm.models import User
from ...schemas.user import (
    CreateUserSchema,
    PublicUserSchema,
)
from ..dependencies import SessionDep

router = APIRouter(prefix='/users', tags=['users'])
password_hash = PasswordHash.recommended()


@router.get('', response_model=list[PublicUserSchema])
async def get_users(
    session: SessionDep,
    offset: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=100),
):
    results = await session.scalars(
        select(User).order_by(User.id).offset(offset).limit(limit)
    )
    return results.all()


@router.post('', response_model=PublicUserSchema, status_code=status.HTTP_201_CREATED)
async def create_user(data: CreateUserSchema, session: SessionDep):
    values = data.model_dump(exclude={'password'})
    user = User(**values, password=password_hash.hash(data.password))
    session.add(user)
    try:
        await session.commit()
    except IntegrityError as error:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='Username already exists',
        ) from error
    await session.refresh(user)
    return user
