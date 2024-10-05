# ---------------------------------------------------------------------------------
#  /\_/\  🌐 This module was loaded through https://t.me/hikkamods_bot
# ( o.o )  🔓 Not licensed.
#  > ^ <   ⚠️ Owner of heta.hikariatama.ru doesn't take any responsibilities or intellectual property rights regarding this script
# ---------------------------------------------------------------------------------
# Name: Online
# Description: Вечный онлайн, который будет читать сообщения в чатах.
# meta developer: @nobianermodules
# Commands:
# .online
# ---------------------------------------------------------------------------------


# @Sekai_Yoneya

from asyncio import sleep

from .. import loader


@loader.tds
class EternalOnlineMod(loader.Module):
    """Вічний онлайн, який буде читати повідомлення в чатах."""

    strings = {"name": "Online"}

    async def client_ready(self, client, db):
        self.db = db

    async def onlinecmd(self, message):
        """Увімкнути вічний онлайн"""
        if not self.db.get("Eternal Online", "status"):
            self.db.set("Eternal Online", "status", True)
            await message.edit("<b>Вічний онлайн увімкнено</b>")
            while self.db.get("Eternal Online", "status"):
                msg = await message.client.send_message(
                    "me", "Telegram best messenger! 🤩"
                )
                await msg.delete()
                await sleep(1000)

        else:
            self.db.set("Eternal Online", "status", False)
            await message.edit("<b>Вічний онлайн вимкнено</b>")

    async def watcher(self, message):
        if self.db.get("Eternal Online", "status"):
            await message.client.send_read_acknowledge(
                message.chat_id, clear_mentions=True
            )
