import pytest
import pytest_asyncio
# from fastapi.testclient import TestClient
from asgi_lifespan import LifespanManager
from httpx import AsyncClient, ASGITransport
from src.app import app
from src.db.database import engine, Base

@pytest.fixture(scope="session", autouse=True)
async def prepare_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()

# @pytest.fixture(scope="session")
# def client():
#     with TestClient(app) as c:
#         yield c

@pytest_asyncio.fixture
async def async_client():
    transport = ASGITransport(app=app)
    async with LifespanManager(app):
        async with AsyncClient(
            transport=transport, base_url="http://test") as ac:
            yield ac

@pytest.fixture
async def db_session():
    from src.db.database import SessionLocal
    async with SessionLocal() as session:
        yield session
        await session.close()
    