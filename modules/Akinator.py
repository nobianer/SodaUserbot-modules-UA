# ---------------------------------------------------------------------------------
#  /\_/\  🌐 This module was loaded through https://t.me/hikkamods_bot
# ( o.o )  🔐 Licensed under the GNU AGPLv3.
#  > ^ <   ⚠️ Owner of heta.hikariatama.ru doesn't take any responsibilities or intellectual property rights regarding this script
# ---------------------------------------------------------------------------------
# Name: akinator
# Author: Den4ikSuperOstryyPer4ik
# Commands:
# .akinator
# ---------------------------------------------------------------------------------

__version__ = (1, 0, 5)
#
# 	 @@@@@@    @@@@@@   @@@@@@@  @@@@@@@    @@@@@@   @@@@@@@@@@    @@@@@@   @@@@@@@   @@@  @@@  @@@       @@@@@@@@   @@@@@@
# 	@@@@@@@@  @@@@@@@   @@@@@@@  @@@@@@@@  @@@@@@@@  @@@@@@@@@@@  @@@@@@@@  @@@@@@@@  @@@  @@@  @@@       @@@@@@@@  @@@@@@@
# 	@@!  @@@  !@@         @@!    @@!  @@@  @@!  @@@  @@! @@! @@!  @@!  @@@  @@!  @@@  @@!  @@@  @@!       @@!       !@@
# 	!@!  @!@  !@!         !@!    !@!  @!@  !@!  @!@  !@! !@! !@!  !@!  @!@  !@!  @!@  !@!  @!@  !@!       !@!       !@!
# 	@!@!@!@!  !!@@!!      @!!    @!@!!@!   @!@  !@!  @!! !!@ @!@  @!@  !@!  @!@  !@!  @!@  !@!  @!!       @!!!:!    !!@@!!
# 	!!!@!!!!   !!@!!!     !!!    !!@!@!    !@!  !!!  !@!   ! !@!  !@!  !!!  !@!  !!!  !@!  !!!  !!!       !!!!!:     !!@!!!
# 	!!:  !!!       !:!    !!:    !!: :!!   !!:  !!!  !!:     !!:  !!:  !!!  !!:  !!!  !!:  !!!  !!:       !!:            !:!
# 	:!:  !:!      !:!     :!:    :!:  !:!  :!:  !:!  :!:     :!:  :!:  !:!  :!:  !:!  :!:  !:!   :!:      :!:           !:!
# 	::   :::  :::: ::      ::    ::   :::  ::::: ::  :::     ::   ::::: ::   :::: ::  ::::: ::   :: ::::   :: ::::  :::: ::
# 	 :   : :  :: : :       :      :   : :   : :  :    :      :     : :  :   :: :  :    : :  :   : :: : :  : :: ::   :: : :
#
#                                             © Copyright 2023
#
#                                    https://t.me/Den4ikSuperOstryyPer4ik
#                                                  and
#                                          https://t.me/ToXicUse
#
#                                    🔒 Licensed under the GNU AGPLv3
#                                 https://www.gnu.org/licenses/agpl-3.0.html
#
# meta banner: https://0x0.st/HQ7s.jpg
# meta developer: @AstroModules

import random

import akinator
import deep_translator

from .. import loader, utils
from ..inline.types import InlineCall

aki_photo = "https://graph.org/file/3cc8825c029fd0cab9edc.jpg"
aki_failed = "https://0x0.st/H1rk.jpg"
emojies = ["😏", "🫢", "🤔", "🫣", "🫤", "😉", "😒"]


@loader.tds
class AkinatorGame(loader.Module):
    """
    Акинатор угадает любого вами загаданного персонажа,
    стоит лишь ответить на пару вопросов)
    """

    strings = {"name": "Akinator"}

    async def client_ready(self):
        self.games = {}

    @loader.command()
    async def akinator(self, message):
        """- начать игру"""
        sta = akinator.Akinator()
        self.games.update({message.chat_id: {message.id: sta}})
        await self.inline.form(
            message=message,
            photo=aki_photo,
            text=(
                "🔮 <b>Задумайте реального або вигаданого персонажа, і натисніть"
                " почати</b>"
            ),
            reply_markup={
                "text": "Почати",
                "callback": self.doai,
                "args": (message,),
            },
        )

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "child_mode",
                True,
                lambda: (
                    "Дитячий режим. Якщо ввімкнений, то буде складніше відгадати 18+ героїв"
                ),
                validator=loader.validators.Boolean(),
            )
        )

    async def doai(self, call: InlineCall, message):
        chat_id = int(message.chat_id)
        mid = int(message.id)
        if self.config["child_mode"]:
            qu = self.games[chat_id][mid].start_game(child_mode=True)
        else:
            qu = self.games[chat_id][mid].start_game(child_mode=False)
        text = deep_translator.GoogleTranslator(source="auto", target="ru").translate(
            qu
        )
        emo = random.choice(emojies)
        await call.edit(
            f"{emo} <b>{text}</b>",
            reply_markup=[
                [
                    {
                        "text": "Так",
                        "callback": self.cont,
                        "args": (
                            "Yes",
                            message,
                        ),
                    },
                    {
                        "text": "Ні",
                        "callback": self.cont,
                        "args": (
                            "No",
                            message,
                        ),
                    },
                    {
                        "text": "Не знаю",
                        "callback": self.cont,
                        "args": (
                            "Idk",
                            message,
                        ),
                    },
                ],
                [
                    {
                        "text": "Можливо",
                        "callback": self.cont,
                        "args": (
                            "Probably",
                            message,
                        ),
                    },
                    {
                        "text": "Скоріше ні",
                        "callback": self.cont,
                        "args": (
                            "Probably Not",
                            message,
                        ),
                    },
                ],
            ],
        )

    async def cont(self, call: InlineCall, args: str, message):
        chat_id = message.chat_id
        mid = message.id
        gm = self.games[chat_id][mid]
        text = gm.answer(args)
        try:
            if gm.progression >= 85:
                gm.win()
                gs = gm.first_guess
                text = f"<b>Это {gs['name']}\n{gs['description']}</b>"
                await call.edit(
                    text,
                    photo=gs["absolute_picture_path"],
                    reply_markup=[
                        {
                            "text": "Це не він",
                            "callback": self.cont,
                            "args": (
                                "No",
                                message,
                            ),
                        },
                    ],
                )
            else:
                text = deep_translator.GoogleTranslator(
                    source="auto", target="ua"
                ).translate(text)
                emo = random.choice(emojies)
                await call.edit(
                    text=f"{emo} <b>{text}</b>",
                    photo=aki_photo,
                    reply_markup=[
                        [
                            {
                                "text": "Так",
                                "callback": self.cont,
                                "args": ("Yes", message),
                            },
                            {
                                "text": "Ні",
                                "callback": self.cont,
                                "args": ("No", message),
                            },
                            {
                                "text": "Не знаю",
                                "callback": self.cont,
                                "args": ("Idk", message),
                            },
                        ],
                        [
                            {
                                "text": "Можливо",
                                "callback": self.cont,
                                "args": ("Probably", message),
                            },
                            {
                                "text": "Скоріше ні",
                                "callback": self.cont,
                                "args": ("Probably Not", message),
                            },
                        ],
                    ],
                )
        except akinator.exceptions.AkinatorQuestionOutOfRangeException:
            await call.edit(
                text="<b>На жаль, я не зміг вгадати цього героя(</b>",
                photo=aki_failed,
            )
