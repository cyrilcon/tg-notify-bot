import base64
from pathlib import Path

import pytest

from config import config

CHAT_ID = config.test_chat_id

TEST_FILE_PATH = Path("tests/document.txt")
MESSAGE = TEST_FILE_PATH.read_text(encoding="utf-8")


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
async def data(file_data):
    """
    Fixture to return data.
    """
    data = {
        "chatID": CHAT_ID,
        "message": MESSAGE,
        "documents": [
            file_data,
        ],
    }
    return data
