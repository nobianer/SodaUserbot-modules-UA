# meta developer: @nobianermodules

version = (1, 0, 0)

import asyncio
import re
from telethon.tl.types import Message
from .. import loader, utils

@loader.tds
class ChatGPTfreeMod(loader.Module):
    """
    Безкоштовний модуль для ChatGPT
    https://t.me/Free_of_ChatGPT_bot
    Спочатку запустіть бота і вимкніть сповіщення
    """

    strings = {
        "name": "ChatGPTfree",
        "loading": "<emoji document_id=5325792861885570739>🔄</emoji> Ваш запит обробляється...",
        "no_args": "<emoji document_id=5210952531676504517>🚫</emoji> Не вказано текст для обробки!",
        "start_text": "<b>👤 Ваш запит:</b> {args}\n\n<b><emoji document_id=5355061947316321722>🤖</emoji> ChatGPT:</b>\n",
        "context_text": "❕ Створився новий діалог. Попередні запити видалено.",
    }

    def __init__(self):
        self.name = self.strings["name"]

    async def client_ready(self, client, db):
        self.client = client
        self.db = db
        self.gpt_free = "@Free_of_ChatGPT_bot"

    async def message_q(
        self,
        text: str,
        user_id: int,
        mark_read: bool = False,
        delete: bool = False,
        ignore_answer: bool = False,
    ):
        """Отправляет сообщение и возвращает ответ"""
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

    def clean_response(self, text: str) -> str:
        """
        Видаляє рекламні посилання під відповідями бота.
        """
        cleaned_text = re.sub(r'[\u4e00-\u9fff]+', '', text)  
        cleaned_text = re.sub(r'\(https?:\/\/\S+\)', '', cleaned_text)  
        cleaned_text = cleaned_text.replace("？AI。", "")  
        cleaned_text = cleaned_text.replace("：", "")  
        return cleaned_text.strip()

    async def gptcmd(self, message: Message):
        """
        {text} - опрацювати текст через ChatGPT
        """
        args = utils.get_args_raw(message)

        if not args:
            return await utils.answer(message, self.strings["no_args"])
        await utils.answer(message, self.strings["loading"])

        response = await self.message_q(
            args, self.gpt_free, mark_read=True, delete=True, ignore_answer=False
        )

        # Очищаем ответ от китайских символов, ссылок и специфичных фраз
        cleaned_response = self.clean_response(response.text)

        text = self.strings["start_text"].format(args=args) + cleaned_response.replace(
            "/context", "<code>.contextgpt</code>"
        )

        return await utils.answer(message, text)

    async def contextgptcmd(self, message: Message):
        """
        - скинути діалог і розпочати новий
        """
        await self.message_q(
            "/context", self.gpt_free, mark_read=True, delete=True, ignore_answer=True
        )
        return await utils.answer(message, self.strings["context_text"])
