import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession

from database.session import session_manager
from main import app


@pytest_asyncio.fixture(scope="function")
async def client(db_session: AsyncSession):
    """Creates an HTTP client for tests."""
    app.dependency_overrides[session_manager.session_getter] = lambda: db_session
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as client:
        yield client
