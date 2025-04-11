from datetime import datetime, timezone
from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import Document, Notification, NotificationDocument


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
        for doc in documents:
            stmt = select(Document).where(
                Document.name == doc.name, Document.buffer == doc.buffer
            )
            result = await session.execute(stmt)
            existing_doc = result.scalars().first()

            if existing_doc:
                document = existing_doc
            else:
                document = Document(
                    name=doc.name,
                    buffer=doc.buffer,
                )
                session.add(document)
                await session.flush()

            session.add(
                NotificationDocument(
                    notification_id=notification.id, document_id=document.id
                )
            )

    await session.commit()
    return notification
