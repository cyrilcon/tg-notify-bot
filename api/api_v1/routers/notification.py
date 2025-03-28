from fastapi import APIRouter, status, Depends, HTTPException, Security
from fastapi.security.api_key import APIKeyHeader
from sqlalchemy.ext.asyncio import AsyncSession

from api.api_v1.crud import create_notification
from api.api_v1.models import NotificationResponse, NotificationRequest
from api.api_v1.services import generate_token
from config import config
from database import session_manager
from tg_bot.bot import BotService

router = APIRouter(tags=[config.api.tags.notification])

api_key_header = APIKeyHeader(name="Authorization")


@router.post(
    "/notify",
    response_model=NotificationResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Send a notification",
    response_description="Notification was sent",
)
async def send_notification(
    notification_in: NotificationRequest,
    token: str = Security(api_key_header),
    session: AsyncSession = Depends(session_manager.session_getter),
):
    """
    Send a notification:

    - `chatID` (Integer): ID of the chat or channel where the message will be sent
    - `message` (String): Message body in Markdown_v2 format
    - `buttonUrl` (String | Null): Optional URL for an inline button in the message
    - `documents` (Array of Document objects | Null)
        - `buffer` (String): File in Base64 format
        - `name` (String): Document name
    """
    generated_token = generate_token()
    if token != generated_token:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid token",
        )

    notification, error = await create_notification(
        session=session,
        notification_in=notification_in,
    )

    if not notification:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create notification in the database: {error}",
        )

    success, error = await BotService.send_message(
        chat_id=notification_in.chatID,
        text=notification_in.message,
        button_url=notification_in.buttonUrl,
        files=notification_in.documents,
    )

    return NotificationResponse(
        success=success,
        errorMessage=error,
        createdAt=notification.created_at,
    )
