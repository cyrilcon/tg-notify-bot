from fastapi import status
from httpx import AsyncClient

from api.api_v1.services import generate_token
from config import config

PREFIX = config.api.prefix + config.api.v1.prefix + "/notify"


class TestSuccess:
    """Tests of successful messaging."""

    async def test_send_message_without_file(self, client: AsyncClient, base_data):
        """Sending a message without a file."""
        token = generate_token()
        headers = {"Authorization": token}

        response = await client.post(url=PREFIX, json=base_data, headers=headers)

        assert response.status_code == status.HTTP_201_CREATED
        assert response.json()["success"] is True
        assert response.json()["errorMessage"] is None
        assert response.json()["createdAt"] is not None

    async def test_send_message_with_file(self, client: AsyncClient, data_with_file):
        """Sending a message with a file."""
        token = generate_token()
        headers = {"Authorization": token}

        response = await client.post(url=PREFIX, json=data_with_file, headers=headers)

        assert response.status_code == status.HTTP_201_CREATED
        assert response.json()["success"] is True
        assert response.json()["errorMessage"] is None
        assert response.json()["createdAt"] is not None

    async def test_send_message_with_button_without_file(
        self, client: AsyncClient, data_with_button
    ):
        """Sending a message with an inline button but without a file."""
        token = generate_token()
        headers = {"Authorization": token}

        response = await client.post(url=PREFIX, json=data_with_button, headers=headers)

        assert response.status_code == status.HTTP_201_CREATED
        assert response.json()["success"] is True
        assert response.json()["errorMessage"] is None
        assert response.json()["createdAt"] is not None

    async def test_send_message_with_button_with_file(
        self, client: AsyncClient, data_with_button_and_file
    ):
        """Sending a message with an inline button and a file."""
        token = generate_token()
        headers = {"Authorization": token}

        response = await client.post(
            url=PREFIX, json=data_with_button_and_file, headers=headers
        )

        assert response.status_code == status.HTTP_201_CREATED
        assert response.json()["success"] is True
        assert response.json()["errorMessage"] is None
        assert response.json()["createdAt"] is not None


class TestAdminsFailure:
    """Tests of errors when sending notifications."""

    async def test_send_notification_missing_token(
        self, client: AsyncClient, base_data
    ):
        """Attempting to send without a token."""
        response = await client.post(url=PREFIX, json=base_data)

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.json()["detail"] == "Not authenticated"

    async def test_send_notification_invalid_token(
        self, client: AsyncClient, base_data
    ):
        """Attempting to send with an invalid token."""
        headers = {"Authorization": "invalid_token"}

        response = await client.post(url=PREFIX, json=base_data, headers=headers)

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.json()["detail"] == "Invalid token"

    async def test_send_notification_missing_chat_id(
        self, client: AsyncClient, base_data
    ):
        """Sending without chat_id."""
        token = generate_token()
        headers = {"Authorization": token}

        data = {**base_data}
        del data["chatID"]

        response = await client.post(url=PREFIX, json=data, headers=headers)

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    async def test_send_notification_missing_message(
        self, client: AsyncClient, base_data
    ):
        """Sending without message."""
        token = generate_token()
        headers = {"Authorization": token}

        data = {**base_data}
        del data["message"]

        response = await client.post(url=PREFIX, json=data, headers=headers)

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    async def test_send_notification_invalid_chat_id(
        self, client: AsyncClient, base_data
    ):
        """Sending with invalid chat_id."""
        token = generate_token()
        headers = {"Authorization": token}

        data = {
            **base_data,
            "chatID": "invalid_chat_id",
        }

        response = await client.post(url=PREFIX, json=data, headers=headers)

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
