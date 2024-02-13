#             █ █ ▀ █▄▀ ▄▀█ █▀█ ▀
#             █▀█ █ █ █ █▀█ █▀▄ █
#              © Copyright 2022
#           https://t.me/hikariatama
#
# 🔒      Licensed under the GNU AGPLv3
# 🌐 https://www.gnu.org/licenses/agpl-3.0.html

# meta pic: https://static.dan.tatar/musicdl_icon.png
# meta banner: https://mods.hikariatama.ru/badges/musicdl.jpg
# meta developer: @hikarimods
# scope: hikka_only
# scope: hikka_min 1.3.0

from telethon.tl.types import Message

from .. import loader, utils


@loader.tds
class MusicDLMod(loader.Module):
    """Завантажує музику"""

    strings = {
        "name": "MusicDL",
        "args": "🚫 <b>Arguments not specified</b>",
        "loading": "🔍 <b>Loading...</b>",
        "404": "🚫 <b>Music </b><code>{}</code><b> not found</b>",
    }

    strings_ua = {
        "args": "🚫 <b>Не вказані аргументи</b>",
        "loading": "🔍 <b>Завантаження...</b>",
        "404": "🚫 <b>Пісню </b><code>{}</code><b> не знайдено</b>",
    }

    async def client_ready(self, *_):
        self.musicdl = await self.import_lib(
            "https://libs.hikariatama.ru/musicdl.py",
            suspend_on_error=True,
        )

    @loader.command(ru_doc="<название> - Завантажити пісню")
    async def mdl(self, message: Message):
        """<name> - Завантажити трек"""
        args = utils.get_args_raw(message)
        if not args:
            await utils.answer(message, self.strings("args"))
            return

        message = await utils.answer(message, self.strings("loading"))
        result = await self.musicdl.dl(args, only_document=True)

        if not result:
            await utils.answer(message, self.strings("404").format(args))
            return

        await self._client.send_file(
            message.peer_id,
            result,
            caption=f"🎧 {utils.ascii_face()}",
            reply_to=getattr(message, "reply_to_msg_id", None),
        )
        if message.out:
            await message.delete()
