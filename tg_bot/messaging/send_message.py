from typing import List, Tuple

from database.models import Document
from tg_bot.bot import bot
from tg_bot.messaging import send_files


async def send_message(
    chat_id: int,
    text: str,
    files: List[Document] = None,
) -> Tuple[bool, str | None]:
    """
    Send files with a caption in one message (album).

    :param chat_id: Telegram chat id.
    :param text: Text to send.
    :param files: List of files to send.
    :return: True if successful, otherwise False and an error message.
    """
    try:
        if files:
            await send_files(chat_id, text, files)
        else:
            await bot.send_message(chat_id, text)
        return True, None
    except Exception as e:
        return False, str(e)
