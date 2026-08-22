from unittest.mock import AsyncMock, Mock

import pytest

from core.api.routers.user import create_user, password_hash
from core.orm.models import User
from core.schemas.user import CreateUserSchema


@pytest.mark.asyncio
async def test_create_user_hashes_password() -> None:
    session = AsyncMock()
    session.add = Mock()
    session.refresh.side_effect = lambda user: setattr(user, 'id', 1)
    password = 'correct-horse-battery-staple'

    result = await create_user(
        CreateUserSchema(
            username='alice',
            first_name='Alice',
            password=password,
        ),
        session,
    )

    added_user = session.add.call_args.args[0]
    assert isinstance(result, User)
    assert added_user.password != password
    assert password_hash.verify(password, added_user.password)
    session.commit.assert_awaited_once()
