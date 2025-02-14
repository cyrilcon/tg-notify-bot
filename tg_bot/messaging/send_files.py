from typing import List

from database.models import Document
from tg_bot.bot import bot
from tg_bot.utils import create_media_group


async def send_files(
    chat_id: int,
    text: str,
    files: List[Document],
) -> None:
    """
    Send files in groups of 10 as albums.

    :param chat_id: Telegram chat id.
    :param text: Text to send.
    :param files: List of files to send.
    """
    # Divide files into groups of 10
    for i in range(0, len(files), 10):
        media_group = create_media_group(files[i : i + 10])

        # If it's the last group and there is text, add it to the last file
        if i + 10 >= len(files) and text:
            media_group[-1].caption = text

        await bot.send_media_group(chat_id, media_group)
