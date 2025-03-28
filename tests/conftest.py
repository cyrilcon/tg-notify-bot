__all__ = (
    "client",
    "file_data",
    "base_data",
    "data_with_button",
    "data_with_file",
    "data_with_button_and_file",
    "setup_database",
    "db_session",
    "event_loop",
)

import asyncio

import pytest_asyncio

from fixtures import (
    client,
    file_data,
    base_data,
    data_with_button,
    data_with_file,
    data_with_button_and_file,
    setup_database,
    db_session,
)


@pytest_asyncio.fixture(scope="session")
async def event_loop():
    """Creates an event loop for the entire test session."""
    loop = asyncio.get_event_loop()
    yield loop
