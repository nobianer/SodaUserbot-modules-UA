# meta developer: @nobianermodules
import asyncio
import random

from telethon.tl.types import Message
from .. import loader, utils

@loader.tds
class VideoDownloader(loader.Module):
    """
    Модуль для завантаження відео за допомогою бота @uasaverbot. Для початку роботи пропишіть /start у боті та вимкніть сповіщення
    """

    strings = {
        "name": "VideoDownloader",
        "waiting_videodl": [
            "📥 Завантажую..."
        ],
        "no_response": "<emoji document_id=5210952531676504517>🚫</emoji> Не вдалося завантатжити відео"
    }

    async def client_ready(self, client, db):
        self.client = client
        self.db = db
        self.target_bot = "@uasaverbot"

    async def send_command(self, command: str, message: Message, waiting_messages: list):
        """Надсилає команду боту та редагує повідомлення очікування"""
        async with self.client.conversation(self.target_bot) as conv:
            await conv.send_message(command)
            waiting_message = random.choice(waiting_messages)
            await utils.answer(message, waiting_message)
            while True:
                response = await conv.get_response()
                if response:
                    await self.client.send_message(message.peer_id, response.text, file=response.media)
                    return
                await asyncio.sleep(1)

    async def videodlcmd(self, message: Message):
        """- .videodl <посилання>"""
        args = utils.get_args_raw(message)
        if not args:
            return await utils.answer(message, self.strings["no_response"])
        command = f"{args}"
        await self.send_command(command, message, self.strings["waiting_videodl"])