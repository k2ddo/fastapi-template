from datetime import UTC, datetime, timedelta
from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from pwdlib import PasswordHash
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..orm.models import User
from ..settings import settings
from .dependencies import SessionDep

password_hash = PasswordHash.recommended()
dummy_password_hash = password_hash.hash('dummy-password-used-for-timing-only')
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f'{settings.API_PREFIX}/auth/token')


def create_access_token(user_id: int) -> str:
    expires_at = datetime.now(UTC) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    return jwt.encode(
        {'sub': str(user_id), 'exp': expires_at},
        settings.JWT_SECRET_KEY.get_secret_value(),
        algorithm='HS256',
    )


async def authenticate_user(
    session: AsyncSession, username: str, password: str
) -> User | None:
    user = await session.scalar(select(User).where(User.username == username))
    if user is None:
        password_hash.verify(password, dummy_password_hash)
        return None
    if not password_hash.verify(password, user.password):
        return None
    return user


def credentials_error() -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'},
    )


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)], session: SessionDep
) -> User:
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY.get_secret_value(),
            algorithms=['HS256'],
        )
        user_id = int(payload['sub'])
    except (InvalidTokenError, KeyError, TypeError, ValueError) as error:
        raise credentials_error() from error

    user = await session.get(User, user_id)
    if user is None:
        raise credentials_error()
    return user


CurrentUserDep = Annotated[User, Depends(get_current_user)]
