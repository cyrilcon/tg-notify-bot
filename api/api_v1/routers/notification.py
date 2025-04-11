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
    "/notification",
    response_model=NotificationResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Send a notification",
    response_description="Notification was sent",
)
async def post_notification(
    notification_request: NotificationRequest,
    token: str = Security(api_key_header),
    session: AsyncSession = Depends(session_manager.session_getter),
):
    """
    Send a notification:

    - `chatIds` (Array of integers): List of chat or channel IDs where the message will be sent
    - `message` (String): Message body in MarkdownV2 format
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

    if not notification_request.chatIds:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="chatIds must not be empty",
        )

    created_at = None
    for chat_id in notification_request.chatIds:
        try:
            notification = await create_notification(
                session=session,
                chat_id=chat_id,
                message=notification_request.message,
                button_url=notification_request.buttonUrl,
                documents=notification_request.documents,
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"DB error: {str(e)}",
            )

        try:
            await BotService.send_message(
                chat_id=chat_id,
                text=notification_request.message,
                button_url=notification_request.buttonUrl,
                files=notification_request.documents,
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail=f"BOT error: {str(e)}",
            )

        # Use the latest time for the answer
        created_at = notification.created_at

    return NotificationResponse(
        chatIds=notification_request.chatIds,
        message=notification_request.message,
        buttonUrl=notification_request.buttonUrl,
        documents=notification_request.documents,
        createdAt=created_at,
    )
