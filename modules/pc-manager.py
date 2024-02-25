# ---------------------------------------------------------------------------------
#  /\_/\  🌐 This module was loaded through https://t.me/hikkamods_bot
# ( o.o )  🔐 Licensed under the GNU AGPLv3.
#  > ^ <   ⚠️ Owner of heta.hikariatama.ru doesn't take any responsibilities or intellectual property rights regarding this script
# ---------------------------------------------------------------------------------
# Name: pcmanager
# Author: Den4ikSuperOstryyPer4ik
# Commands:
# .addbot | .tutor   | .pcoff | .pcreboot   | .pcinfo 
# .pcip   | .pcscrin | .pcweb | .pcwebscrin | .pcalert
# .pcvol  | .pcmedia
# ---------------------------------------------------------------------------------

# =^..^= Proxied library: https://raw.githubusercontent.com/ToXic2290/Hikka-moduless/main/AstroModules_Library.py -> https://heta.hikariatama.ru/libs/shino_qAwcGboUzKDqdrsjXAGg.py

__version__ = (1, 0, 0)
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
# meta developer: @AstroModules

from telethon.tl.types import Message

from .. import loader, utils
from ..inline.types import InlineCall


class PCManagerMod(loader.Module):
    """Керування вашим комп'ютером за допомогою юзербота"""

    strings = {"name": "PC-Manager"}

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "bot_username",
                None,
                doc=lambda: "Введіть юзернейм вашого бота для керування ПК",
            )
        )

    async def client_ready(self):
        self.lib = await self.import_lib(
            "https://raw.githubusercontent.com/ToXic2290/Hikka-moduless/main/AstroModules_Library.py",
            suspend_on_error=False,
        )

    @loader.command()
    async def addbot(self, message: Message):
        """- додати бота

        💎 Основні команди:"""
        await self.allmodules.commands["config"](
            await utils.answer(message, f"{self.get_prefix()}config PC-Manager")
        )

    @loader.command()
    async def tutor(self, message: Message):
        """- туторіал з ідключення"""
        await utils.answer(
            message,
            (
                "<emoji document_id=5787237370709413702>⚙️</emoji> <b>Туторіал з"
                " налаштування модуля:</b>\n\n@PC_AM_Tutor\n\nЯкщо виникли труднощі з"
                " встановленням, будь ласка, зверніться до чату AstroModules "
            ),
        )

    @loader.command()
    async def pcoff(self, message: Message):
        """- вимкнути комп'ютер"""
        bot = self.config["bot_username"]
        call = await self.lib.message_g(f"🛑 Shutdown", bot, mark_read=True, delete=True)
        await utils.answer(
            message,
            (
                "<emoji document_id=5787544344906959608>ℹ️</emoji> <b>[PC_Manager]</b>"
                f" <emoji document_id=5787544344906959608>ℹ️</emoji>\n\n{call.text}"
            ),
        )

    @loader.command()
    async def pcreboot(self, message: Message):
        """- перезавантажити комп'ютер"""
        bot = self.config["bot_username"]
        call = await self.lib.message_g(f"🔄 Reboot", bot, mark_read=True, delete=True)
        await utils.answer(
            message,
            (
                "<emoji document_id=5787544344906959608>ℹ️</emoji> <b>[PC_Manager]</b>"
                f" <emoji document_id=5787544344906959608>ℹ️</emoji>\n\n{call.text}"
            ),
        )

    @loader.command()
    async def pcinfo(self, message: Message):
        """- подивитись характеристики системи"""
        bot = self.config["bot_username"]
        call = await self.lib.message_q(
            f"💻 System Info", bot, mark_read=True, delete=True
        )
        await utils.answer(
            message,
            (
                "<emoji document_id=5787544344906959608>ℹ️</emoji> <b>[PC_Manager]</b>"
                f" <emoji document_id=5787544344906959608>ℹ️</emoji>\n\n{call.text}"
            ),
        )

    @loader.command()
    async def pcip(self, message: Message):
        """- подивитись інформацію про IP-адресу"""
        bot = self.config["bot_username"]
        call = await self.lib.message_q(f"🌐 IP Info", bot, mark_read=True, delete=True)
        await utils.answer(
            message,
            (
                "<emoji document_id=5787544344906959608>ℹ️</emoji> <b>[PC_Manager]</b>"
                f" <emoji document_id=5787544344906959608>ℹ️</emoji>\n\n{call.text}"
            ),
        )

    @loader.command()
    async def pcscrin(self, message: Message):
        """- зробити скріншот екрану"""
        bot = self.config["bot_username"]
        call = await self.lib.message_g(
            f"/screenshot", bot, mark_read=True, delete=True
        )
        await utils.answer(
            message,
            (
                f"<emoji document_id=5787544344906959608>ℹ️</emoji> <b>[PC_Manager]</b>"
                f" <emoji document_id=5787544344906959608>ℹ️</emoji>\n\nНадсилання"
                f" скріншоту..."
            ),
        )
        await message.respond(call)

    @loader.command()
    async def pcweb(self, message: Message):
        """<посилання> - відкрити посилання в браузері"""
        bot = self.config["bot_username"]
        args = utils.get_args_raw(message)
        call = await self.lib.message_q(
            f"/browse {args}", bot, mark_read=True, delete=True
        )
        await utils.answer(
            message,
            (
                "<emoji document_id=5787544344906959608>ℹ️</emoji> <b>[PC_Manager]</b>"
                " <emoji"
                f" document_id=5787544344906959608>ℹ️</emoji>\n\n{call.text}\n\nПосилання:"
                f" {args}"
            ),
        )

    @loader.command()
    async def pcwebscrin(self, message: Message):
        """- зробити знімок з веб-камери

        🔑 Додатково:"""
        bot = self.config["bot_username"]
        call = await self.lib.message_g(f"/photo", bot, mark_read=True, delete=True)
        await utils.answer(
            message,
            (
                f"<emoji document_id=5787544344906959608>ℹ️</emoji> <b>[PC_Manager]</b>"
                f" <emoji document_id=5787544344906959608>ℹ️</emoji>\n\nНадсилання"
                f" знімку..."
            ),
        )
        await message.respond(call)

    @loader.command()
    async def pcalert(self, message: Message):
        """<повідомлення> - вивести на екран повідомлення"""
        bot = self.config["bot_username"]
        args = utils.get_args_raw(message)
        call = await self.lib.message_q(
            f"/alert {args}", bot, mark_read=True, delete=True
        )
        await message.respond(
            "<emoji document_id=5787544344906959608>ℹ️</emoji> <b>[PC_Manager]</b>"
            f" <emoji document_id=5787544344906959608>ℹ️</emoji>\n\n{call.text}"
        )
        await message.delete()

    @loader.command()
    async def pcvol(self, message: Message):
        """- керування звуком"""
        await self.inline.form(
            text="ℹ️ <b>[PC_Manager]</b> ℹ️\n\n<b>Мішкер гучності</b>",
            reply_markup=[
                [
                    {"text": "10%", "callback": self.vol10},
                    {"text": "20%", "callback": self.vol20},
                    {"text": "30%", "callback": self.vol30},
                ],
                [
                    {"text": "40%", "callback": self.vol40},
                    {"text": "50%", "callback": self.vol50},
                    {"text": "60%", "callback": self.vol60},
                ],
                [
                    {"text": "70%", "callback": self.vol70},
                    {"text": "80%", "callback": self.vol80},
                    {"text": "90%", "callback": self.vol90},
                ],
                [
                    {"text": "⬆️", "callback": self.volUp},
                    {"text": "100%", "callback": self.vol100},
                    {"text": "⬇️", "callback": self.volDown},
                ],
                [{"text": "🚫 Закрити", "action": "close"}],
            ],
            message=message,
        )

    @loader.command()
    async def pcmedia(self, message: Message):
        """- керування музикою"""
        await self.inline.form(
            text="ℹ️ <b>[PC_Manager]</b> ℹ️\n\n<b>Керування медіа</b>",
            reply_markup=[
                [
                    {"text": "⏪", "callback": self.nazad},
                    {"text": "⏯", "callback": self.pausa},
                    {"text": "⏩", "callback": self.vpered},
                ],
                [{"text": "🚫 Закрити", "action": "close"}],
            ],
            message=message,
        )

    async def nazad(self, call: InlineCall):
        bot = self.config["bot_username"]
        await self.client.send_message(f"{bot}", "/key__prev")
        return await call.answer("Успішно!", show_alert=False)

    async def pausa(self, call: InlineCall):
        bot = self.config["bot_username"]
        await self.client.send_message(f"{bot}", "/key__play")
        return await call.answer("Успішно!", show_alert=False)

    async def vpered(self, call: InlineCall):
        bot = self.config["bot_username"]
        await self.client.send_message(f"{bot}", "/key__next")
        return await call.answer("Успішно!", show_alert=False)

    async def vol10(self, call: InlineCall):
        bot = self.config["bot_username"]
        await self.client.send_message(f"{bot}", "/volume 10")
        return await call.answer("Успішно!", show_alert=False)

    async def vol20(self, call: InlineCall):
        bot = self.config["bot_username"]
        await self.client.send_message(f"{bot}", "/volume 20")
        return await call.answer("Успішно!", show_alert=False)

    async def vol30(self, call: InlineCall):
        bot = self.config["bot_username"]
        await self.client.send_message(f"{bot}", "/volume 30")
        return await call.answer("Успішно!", show_alert=False)

    async def vol40(self, call: InlineCall):
        bot = self.config["bot_username"]
        await self.client.send_message(f"{bot}", "/volume 40")
        return await call.answer("Успішно!", show_alert=False)

    async def vol50(self, call: InlineCall):
        bot = self.config["bot_username"]
        await self.client.send_message(f"{bot}", "/volume 50")
        return await call.answer("Успішно!", show_alert=False)

    async def vol60(self, call: InlineCall):
        bot = self.config["bot_username"]
        await self.client.send_message(f"{bot}", "/volume 60")
        return await call.answer("Успішно!", show_alert=False)

    async def vol70(self, call: InlineCall):
        bot = self.config["bot_username"]
        await self.client.send_message(f"{bot}", "/volume 70")
        return await call.answer("Успішно!", show_alert=False)

    async def vol80(self, call: InlineCall):
        bot = self.config["bot_username"]
        await self.client.send_message(f"{bot}", "/volume 80")
        return await call.answer("Успішно!", show_alert=False)

    async def vol90(self, call: InlineCall):
        bot = self.config["bot_username"]
        await self.client.send_message(f"{bot}", "/volume 90")
        return await call.answer("Успішно!", show_alert=False)

    async def vol100(self, call: InlineCall):
        bot = self.config["bot_username"]
        await self.client.send_message(f"{bot}", "/volume 100")
        return await call.answer("Успішно!", show_alert=False)

    async def volUp(self, call: InlineCall):
        bot = self.config["bot_username"]
        await self.client.send_message(f"{bot}", "/volume up")
        return await call.answer("Успішно!", show_alert=False)

    async def volDown(self, call: InlineCall):
        bot = self.config["bot_username"]
        await self.client.send_message(f"{bot}", "/volume down")
        return await call.answer("Успішно!", show_alert=False)

        # Tx...