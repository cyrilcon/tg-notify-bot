import base64
from typing import List

from aiogram.types import BufferedInputFile, InputMediaDocument

from database.models import Document


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
