from typing import cast

import pytest
from starlette.requests import Request

from core.admin.auth import authentication_backend


class FakeRequest:
    def __init__(self, username: str, password: str) -> None:
        self.username = username
        self.password = password
        self.session: dict[str, bool] = {}

    async def form(self) -> dict[str, str]:
        return {'username': self.username, 'password': self.password}


@pytest.mark.asyncio
async def test_admin_authentication() -> None:
    invalid_request = cast(Request, FakeRequest('admin', 'wrong-password'))
    assert await authentication_backend.login(invalid_request) is False
    assert await authentication_backend.authenticate(invalid_request) is False

    valid_request = cast(Request, FakeRequest('admin', 'test-admin-password'))
    assert await authentication_backend.login(valid_request) is True
    assert await authentication_backend.authenticate(valid_request) is True
