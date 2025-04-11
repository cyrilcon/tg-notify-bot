__all__ = (
    "client",
    "setup_database",
    "db_session",
    "event_loop",
)

import asyncio

import pytest_asyncio

from fixtures import (
    client,
    setup_database,
    db_session,
)


@pytest_asyncio.fixture(scope="session")
async def event_loop():
    """Creates an event loop for the entire test session."""
    loop = asyncio.get_event_loop()
    yield loop
