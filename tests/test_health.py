import pytest
from httpx import ASGITransport, AsyncClient

from core.api.api import app


@pytest.mark.asyncio
async def test_liveness() -> None:
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url='http://test'
    ) as client:
        response = await client.get('/health/live')

    assert response.status_code == 200
    assert response.json() == {'status': 'ok'}
