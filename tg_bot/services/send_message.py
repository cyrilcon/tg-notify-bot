import base64
from typing import List, Tuple

from aiogram.types import BufferedInputFile, InputMediaDocument

from database.models import Document
from tg_bot.bot import bot


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


def create_media_group(files: List[Document]) -> List[InputMediaDocument]:
    """
    Create a media group for sending.

    :param files: List of files to send.
    :return: List of InputMediaDocument objects.
    """
    media_group = []
    for file in files:
        buffer = base64.b64decode(file.buffer)
        file_obj = BufferedInputFile(file=buffer, filename=file.name)
        media_group.append(InputMediaDocument(media=file_obj))

    return media_group
