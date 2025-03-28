import base64
from pathlib import Path

import pytest

from config import config

CHAT_ID = config.test_chat_id
TEST_FILE_PATH = Path("tests/document.txt")
MESSAGE = TEST_FILE_PATH.read_text(encoding="utf-8")
BUTTON_URL = "https://example.com"


@pytest.fixture(scope="function")
def file_data():
    """Fixture for loading a file in base64."""
    file_path = Path("tests/document.txt")
    file_name = file_path.name

    with open(file_path, "rb") as file:
        buffer_file = base64.b64encode(file.read()).decode("utf-8")

    return {
        "buffer": buffer_file,
        "name": file_name,
    }


@pytest.fixture(scope="function")
async def base_data():
    """Base fixture for testing data."""
    return {
        "chatID": CHAT_ID,
        "message": MESSAGE,
    }


@pytest.fixture(scope="function")
async def data_with_button(base_data):
    """Data fixture with an inline button."""
    return {
        **base_data,
        "buttonUrl": BUTTON_URL,
    }


@pytest.fixture(scope="function")
async def data_with_file(base_data, file_data):
    """Data fixture with a file."""
    return {
        **base_data,
        "documents": [file_data],
    }


@pytest.fixture(scope="function")
async def data_with_button_and_file(base_data, file_data):
    """Data fixture with a file and an inline button."""
    return {
        **base_data,
        "buttonUrl": BUTTON_URL,
        "documents": [file_data],
    }
