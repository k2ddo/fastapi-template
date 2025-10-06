from fastapi import APIRouter
from sqlalchemy import select

from ...orm.models import User
from ...schemas.user import (
    CreateUserSchema,
    PublicUserSchema,
    UpdateUserSchema,
)
from ..dependencies import SessionDep

router = APIRouter()


@router.get('/', response_model=list[PublicUserSchema])
async def get_users(session: SessionDep):
    results = await session.scalars(select(User))
    return results.all()


@router.post('/', response_model=PublicUserSchema)
async def create_user(data: CreateUserSchema, session: SessionDep):
    user = User(**data.model_dump())
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user
