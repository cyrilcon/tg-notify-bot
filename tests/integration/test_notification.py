from fastapi import status
from httpx import AsyncClient

from api.api_v1.services import generate_token
from config import config

PREFIX = config.api.prefix + config.api.v1.prefix + "/"


class TestSuccess:
    """Tests of successful messaging."""

    async def test_send_message_without_file(self, client: AsyncClient, data):
        """Sending a message without a file."""
        token = generate_token()
        headers = {"Authorization": token}

        del data["documents"]

        response = await client.post(url=PREFIX, json=data, headers=headers)

        assert response.status_code == status.HTTP_201_CREATED
        assert response.json()["error"] is None
        assert response.json()["successfully"] is True
        assert response.json()["created_at"] is not None

    async def test_send_message_with_file(self, client: AsyncClient, data):
        """Sending a message with a file."""
        token = generate_token()
        headers = {"Authorization": token}

        response = await client.post(url=PREFIX, json=data, headers=headers)

        assert response.status_code == status.HTTP_201_CREATED
        assert response.json()["successfully"] is True
        assert response.json()["error"] is None
        assert response.json()["created_at"] is not None


class TestAdminsFailure:
    """Tests of errors when sending notifications."""

    async def test_send_notification_missing_token(self, client: AsyncClient, data):
        """Attempting to send without a token."""
        response = await client.post(url=PREFIX, json=data)

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.json()["detail"] == "Not authenticated"

    async def test_send_notification_invalid_token(self, client: AsyncClient, data):
        """Attempting to send with an invalid token."""
        headers = {"Authorization": "invalid_token"}

        response = await client.post(url=PREFIX, json=data, headers=headers)

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.json()["detail"] == "Invalid token"

    async def test_send_notification_missing_chat_id(self, client: AsyncClient, data):
        """Sending without chat_id."""
        token = generate_token()
        headers = {"Authorization": token}

        del data["chat_id"]

        response = await client.post(url=PREFIX, json=data, headers=headers)

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    async def test_send_notification_missing_message(self, client: AsyncClient, data):
        """Sending without message."""
        token = generate_token()
        headers = {"Authorization": token}

        del data["message"]

        response = await client.post(url=PREFIX, json=data, headers=headers)

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    async def test_send_notification_invalid_chat_id(self, client: AsyncClient, data):
        """Sending with invalid chat_id."""
        token = generate_token()
        headers = {"Authorization": token}

        data["chat_id"] = "invalid_chat_id"

        response = await client.post(url=PREFIX, json=data, headers=headers)

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
