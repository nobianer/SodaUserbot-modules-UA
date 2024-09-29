# meta developer: @nobianermodules

version = (1, 0, 0)

import asyncio

from telethon import functions
from telethon.tl.types import Message

from .. import loader, utils


@loader.tds
class SpotifyScannerMod(loader.Module):
    """
    Модуль для виявлення російських артистів Spotify
    https://t.me/spotifyscannerbot
    Спочатку запустіть бота і вимкніть сповіщення
    """

    strings = {
        "name": "SpotifyScanner",
        "loading": "<emoji document_id=5325792861885570739>🔄</emoji> Ваш запит обробляється...",
        "no_args": "<emoji document_id=5210952531676504517>🚫</emoji> Не вказано текст для обробки!",
        "start_text": "<b>Ваш запит:</b> {args}\n\n<b>Відповідь:</b>\n",
        "context_text": "❕ Створився новий діалог. Попередні запити видалено.",
    }

    def __init__(self):
        self.name = self.strings["name"]

    async def client_ready(self, client, db):
        self.client = client
        self.db = db
        self.gpt_free = "@spotifyscannerbot"

    async def message_q(
        self,
        text: str,
        user_id: int,
        mark_read: bool = False,
        delete: bool = False,
        ignore_answer: bool = False,
    ):
        """Надсилає повідомлення і отримує відповідь"""
        async with self.client.conversation(user_id) as conv:
            msg = await conv.send_message(text)
            while True:
                await asyncio.sleep(1)
                response = await conv.get_response()
                if mark_read:
                    await conv.mark_read()
                if delete:
                    await msg.delete()
                    await response.delete()
                if ignore_answer:
                    return response
                if "✅ Запит надіслано" in response.text:
                    continue
                if "Очікування відповіді" in response.text:
                    continue
                return response

    async def scancmd(self, message: Message):
        """
        {text} - перевірити артиста
        """
        args = utils.get_args_raw(message)

        if not args:
            return await utils.answer(message, self.strings["no_args"])
        await utils.answer(message, self.strings["loading"])

        response = await self.message_q(
            args, self.gpt_free, mark_read=True, delete=True, ignore_answer=False
        )

        text = self.strings["start_text"].format(args=args) + response.text.replace(
            "/context", "<code>.contextgpt</code>"
        )

        return await utils.answer(message, text)