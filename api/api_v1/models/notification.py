from datetime import datetime
from typing import List

from pydantic import BaseModel, Field

from .document import Document


class NotificationRequest(BaseModel):
    chatIds: List[int] = Field(
        ...,
        description="List of chat or channel IDs where the message will be sent",
        examples=[[123456789, 987654321]],
    )
    message: str = Field(
        ...,
        description="Message body in MarkdownV2 format",
        examples=["Hello, this is a message with *markdown* formatting"],
    )
    buttonUrl: str | None = Field(
        None,
        description="Optional URL for an inline button in the message. If provided, the message will include a button linking to this URL.",
        examples=["https://example.com"],
    )
    documents: List[Document] | None = Field(
        None,
        description="Optional list of attached documents",
        examples=[
            [
                {"buffer": "SGVsbG8gd29ybGQ=", "name": "Document 1.pdf"},
                {"buffer": "U29tZSBuZXcgZGF0YQ==", "name": "Document 2.pdf"},
            ]
        ],
    )


class NotificationResponse(NotificationRequest):
    createdAt: datetime = Field(
        ...,
        description="Time of notification sending in ISO 8601 format",
        examples=["2024-06-06T12:00:02Z"],
    )
