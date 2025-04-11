import base64
from pathlib import Path

from fastapi import status
from httpx import AsyncClient

from api.api_v1.services import generate_token
from config import config

PREFIX = config.api.prefix + config.api.v1.prefix + "/notification"

CHAT_IDS = [config.test_chat_id]
FILE_PATH = Path("tests/document.txt")
MESSAGE = FILE_PATH.read_text(encoding="utf-8")
BUTTON_URL = "https://example.com"
FILE_NAME = FILE_PATH.name

file = open(FILE_PATH, "rb")
BUFFER_FILE = base64.b64encode(file.read()).decode("utf-8")
file.close()


class TestNotificationSuccess:
    """Successful notification sending."""

    async def test_send__no_file(self, client: AsyncClient):
        """Send message without files or buttons."""
        token = generate_token()
        headers = {"Authorization": token}
        data = {
            "chatIds": CHAT_IDS,
            "message": MESSAGE,
        }

        response = await client.post(url=PREFIX, json=data, headers=headers)

        assert response.status_code == status.HTTP_201_CREATED
        assert response.json().get("message") == data["message"]
        assert response.json().get("createdAt") is not None

    async def test_send__with_file(self, client: AsyncClient):
        """Send message with a file."""
        token = generate_token()
        headers = {"Authorization": token}
        data = {
            "chatIds": CHAT_IDS,
            "message": MESSAGE,
            "documents": [
                {
                    "buffer": BUFFER_FILE,
                    "name": FILE_NAME,
                },
            ],
        }

        response = await client.post(url=PREFIX, json=data, headers=headers)

        assert response.status_code == status.HTTP_201_CREATED
        assert response.json().get("message") == data["message"]
        assert response.json().get("documents") == data["documents"]
        assert response.json().get("createdAt") is not None

    async def test_send__with_button(self, client: AsyncClient):
        """Send message with an inline button."""
        token = generate_token()
        headers = {"Authorization": token}
        data = {
            "chatIds": CHAT_IDS,
            "message": MESSAGE,
            "buttonUrl": BUTTON_URL,
        }

        response = await client.post(url=PREFIX, json=data, headers=headers)

        assert response.status_code == status.HTTP_201_CREATED
        assert response.json().get("message") == data["message"]
        assert response.json().get("buttonUrl") == data["buttonUrl"]
        assert response.json().get("createdAt") is not None

    async def test_send__with_button_and_file(self, client: AsyncClient):
        """Send message with inline button and file."""
        token = generate_token()
        headers = {"Authorization": token}
        data = {
            "chatIds": CHAT_IDS,
            "message": MESSAGE,
            "buttonUrl": BUTTON_URL,
            "documents": [
                {
                    "buffer": BUFFER_FILE,
                    "name": FILE_NAME,
                },
            ],
        }

        response = await client.post(url=PREFIX, json=data, headers=headers)

        assert response.status_code == status.HTTP_201_CREATED
        assert response.json().get("message") == data["message"]
        assert response.json().get("buttonUrl") == data["buttonUrl"]
        assert response.json().get("documents") == data["documents"]
        assert response.json().get("createdAt") is not None


class TestNotificationFailure:
    """Notification error handling."""

    async def test_error__missing_token(self, client: AsyncClient):
        """Fail: no token provided."""
        data = {
            "chatIds": CHAT_IDS,
            "message": MESSAGE,
        }

        response = await client.post(url=PREFIX, json=data)

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.json().get("detail") == "Not authenticated"

    async def test_error__invalid_token(self, client: AsyncClient):
        """Fail: invalid token."""
        headers = {"Authorization": "invalid_token"}
        data = {
            "chatIds": CHAT_IDS,
            "message": MESSAGE,
        }

        response = await client.post(url=PREFIX, json=data, headers=headers)

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.json().get("detail") == "Invalid token"

    async def test_error__missing_chat_ids(self, client: AsyncClient):
        """Fail: missing chatIds."""
        token = generate_token()
        headers = {"Authorization": token}
        data = {
            "message": MESSAGE,
        }

        response = await client.post(url=PREFIX, json=data, headers=headers)

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    async def test_error__missing_message(self, client: AsyncClient):
        """Fail: missing message."""
        token = generate_token()
        headers = {"Authorization": token}
        data = {
            "chatIds": CHAT_IDS,
        }

        response = await client.post(url=PREFIX, json=data, headers=headers)

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    async def test_error__invalid_chat_id_type(self, client: AsyncClient):
        """Fail: chatIds is not list of integers."""
        token = generate_token()
        headers = {"Authorization": token}
        data = {
            "chatIds": ["invalid_chat_id"],
            "message": MESSAGE,
        }

        response = await client.post(url=PREFIX, json=data, headers=headers)

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    async def test_error__empty_chat_ids(self, client: AsyncClient):
        """Fail: chatIds is an empty list."""
        token = generate_token()
        headers = {"Authorization": token}
        data = {
            "chatIds": [],
            "message": MESSAGE,
        }

        response = await client.post(url=PREFIX, json=data, headers=headers)

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        assert response.json().get("detail") == "chatIds must not be empty"
