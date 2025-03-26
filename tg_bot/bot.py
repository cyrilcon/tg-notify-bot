from typing import List, Tuple

from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from config import config
from database.models import Document
from tg_bot.utils import create_media_group


class BotService:
    bot = Bot(
        token=config.tg_bot.token,
        default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN_V2),
    )

    @staticmethod
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
                await BotService.send_files(chat_id, text, files)
            else:
                await BotService.bot.send_message(chat_id, text)
            return True, None
        except Exception as e:
            return False, str(e)

    @staticmethod
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

            await BotService.bot.send_media_group(chat_id, media_group)
