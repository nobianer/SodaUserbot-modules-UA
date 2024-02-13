# ---------------------------------------------------------------------------------
#  /\_/\  🌐 This module was loaded through https://t.me/hikkamods_bot
# ( o.o )  🔐 Licensed under the Copyleft license.
#  > ^ <   ⚠️ Owner of heta.hikariatama.ru doesn't take any responsibilities or intellectual property rights regarding this script
# ---------------------------------------------------------------------------------
# Name: chatgptfree
# Author: vsecoder
# Commands:
# .chatgptfree | .contextgpt
# ---------------------------------------------------------------------------------

"""
                                _             
  __   _____  ___  ___ ___   __| | ___ _ __   
  \ \ / / __|/ _ \/ __/ _ \ / _` |/ _ \ '__|  
   \ V /\__ \  __/ (_| (_) | (_| |  __/ |     
    \_/ |___/\___|\___\___/ \__,_|\___|_|     

    Copyleft 2022 t.me/vsecoder                                                            
    This program is free software; you can redistribute it and/or modify 

"""
# meta developer: @vsecoder_m

version = (1, 0, 0)

import asyncio

from telethon import functions
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
        "loading": "🔄 Ваш запит обробляється...",
        "no_args": "🚫 Не вказано текст для обробки!",
        "start_text": "<b>👤 Ваш запит:</b> {args}\n\n<b>🤖 ChatGPT:</b>\n",
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
        """Отправляет сообщение и возращает ответ"""
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

        text = self.strings["start_text"].format(args=args) + response.text.replace(
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