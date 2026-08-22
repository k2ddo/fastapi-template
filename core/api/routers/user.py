from fastapi import APIRouter, HTTPException, status
from sqlalchemy.exc import IntegrityError

from ...orm.models import User
from ...schemas.user import (
    CreateUserSchema,
    PublicUserSchema,
)
from ..dependencies import SessionDep
from ..security import CurrentUserDep, password_hash

router = APIRouter(prefix='/users', tags=['users'])


@router.get('/me', response_model=PublicUserSchema)
async def get_current_user(user: CurrentUserDep) -> User:
    return user


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
