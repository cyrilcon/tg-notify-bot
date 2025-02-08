from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict

from .document import Document


class NotificationRequest(BaseModel):
    chat_id: int = Field(..., description="ID of the chat or channel")
    message: str = Field(..., description="Message body in markdown format")
    documents: list[Document] | None = Field(None, description="List of documents")


class NotificationResponse(BaseModel):
    successfully: bool = Field(
        ..., description="Indicates if the message was sent successfully"
    )
    error: str | None = Field(
        None, description="Error message if something went wrong, otherwise null"
    )
    created_at: datetime = Field(
        ..., description="Time when the response was generated in ISO 8601 format"
    )
