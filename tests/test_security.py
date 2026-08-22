from unittest.mock import AsyncMock

import jwt
import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from core.api.security import authenticate_user, create_access_token, password_hash
from core.orm.models import User
from core.settings import settings


def test_access_token_contains_user_id() -> None:
    token = create_access_token(42)
    payload = jwt.decode(
        token,
        settings.JWT_SECRET_KEY.get_secret_value(),
        algorithms=['HS256'],
    )

    assert payload['sub'] == '42'
    assert 'exp' in payload


@pytest.mark.asyncio
async def test_authenticate_user_verifies_password() -> None:
    session = AsyncMock(spec=AsyncSession)
    user = User(
        id=1,
        username='alice',
        first_name='Alice',
        last_name=None,
        password=password_hash.hash('correct-horse-battery-staple'),
    )
    session.scalar.return_value = user

    authenticated = await authenticate_user(
        session, 'alice', 'correct-horse-battery-staple'
    )
    rejected = await authenticate_user(session, 'alice', 'wrong-password')

    assert authenticated is user
    assert rejected is None
