from datetime import datetime

from pydantic import BaseModel, Field

from .document import Document


class NotificationRequest(BaseModel):
    chatID: int = Field(..., description="ID of the chat or channel")
    message: str = Field(..., description="Message body in markdown format")
    documents: list[Document] | None = Field(None, description="List of documents")


class NotificationResponse(BaseModel):
    success: bool = Field(
        ..., description="Indicates if the message was sent successfully"
    )
    errorMessage: str | None = Field(
        None, description="Error message if something went wrong, otherwise null"
    )
    createdAt: datetime = Field(
        ..., description="Time when the response was generated in ISO 8601 format"
    )
