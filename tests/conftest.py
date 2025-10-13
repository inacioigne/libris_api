import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from asgi_lifespan import LifespanManager
from httpx import AsyncClient, ASGITransport
from src.app import app

@pytest.fixture(scope="session")
def client():
    with TestClient(app) as c:
        yield c

@pytest_asyncio.fixture
async def async_client():
    transport = ASGITransport(app=app)
    async with LifespanManager(app):
        async with AsyncClient(
            transport=transport, base_url="http://test") as ac:
            yield ac
    