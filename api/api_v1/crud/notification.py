from datetime import datetime, timezone
from typing import Tuple

from sqlalchemy.ext.asyncio import AsyncSession

from api.api_v1.models import NotificationRequest
from database.models import Document, Notification


async def create_notification(
    session: AsyncSession,
    notification_in: NotificationRequest,
) -> Tuple[Notification | None, str | None]:
    """
    Create a new notification and its associated documents in the database.

    :param session: Session for working with the database.
    :param notification_in: Body of the notification request.
    :return: The notification object and None if successful, otherwise None and an error message.
    """
    try:
        notification = Notification(
            chat_id=notification_in.chatID,
            message=notification_in.message,
            button_url=notification_in.buttonUrl,
            created_at=datetime.now(timezone.utc),
        )

        session.add(notification)
        await session.flush()

        documents = notification_in.documents
        if documents:
            for document in documents:
                new_document = Document(
                    notification_id=notification.id,
                    buffer=document.buffer,
                    name=document.name,
                )
                session.add(new_document)

        await session.commit()
        return notification, None

    except Exception as e:
        await session.rollback()
        return None, str(e)
