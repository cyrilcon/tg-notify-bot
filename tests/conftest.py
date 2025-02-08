__all__ = (
    "event_loop",
    "setup_database",
    "db_session",
    "client",
    "file_data",
    "data",
)

import asyncio

import pytest_asyncio

from fixtures import client, file_data, data, setup_database, db_session


@pytest_asyncio.fixture(scope="session")
async def event_loop():
    """Creates an event loop for the entire test session."""
    loop = asyncio.get_event_loop()
    yield loop
