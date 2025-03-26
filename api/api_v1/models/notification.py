from datetime import datetime

from pydantic import BaseModel, Field

from .document import Document


class NotificationRequest(BaseModel):
    chatID: int = Field(
        ...,
        description="ID of the chat or channel",
        examples=[123456789],
    )
    message: str = Field(
        ...,
        description="Message body in markdown format",
        examples=["Hello, this is a message with *markdown* formatting."],
    )
    documents: list[Document] | None = Field(
        None,
        description="List of documents",
        examples=[
            [
                {"buffer": "SGVsbG8gd29ybGQ=", "name": "Document 1.pdf"},
                {"buffer": "U29tZSBuZXcgZGF0YQ==", "name": "Document 2.pdf"},
            ]
        ],
    )


class NotificationResponse(BaseModel):
    success: bool = Field(
        ...,
        description="Indicates if the message was sent successfully",
        examples=[True],
    )
    errorMessage: str | None = Field(
        None,
        description="Error message if something went wrong, otherwise null",
        examples=[None],
    )
    createdAt: datetime = Field(
        ...,
        description="Time when the response was generated in ISO 8601 format",
        examples=["2024-06-06T12:00:02Z"],
    )
