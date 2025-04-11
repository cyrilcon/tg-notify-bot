from datetime import datetime, timezone
from typing import List

from sqlalchemy.ext.asyncio import AsyncSession

from database.models import Document, Notification


async def create_notification(
    session: AsyncSession,
    chat_id: int,
    message: str,
    button_url: str | None = None,
    documents: List[Document] | None = None,
) -> Notification:
    """
    Create a notification in database.

    :param session: Async database session.
    :param chat_id: Telegram chat id.
    :param message: Text to send.
    :param button_url: Optional URL for an inline button in the message.
    :param documents: List of files to send.
    :return: Notification object.
    """
    notification = Notification(
        chat_id=chat_id,
        message=message,
        button_url=button_url,
        created_at=datetime.now(timezone.utc),
    )

    session.add(notification)
    await session.flush()

    if documents:
        for document in documents:
            new_document = Document(
                notification_id=notification.id,
                buffer=document.buffer,
                name=document.name,
            )
            session.add(new_document)

    await session.commit()
    return notification
