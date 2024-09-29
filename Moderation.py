# meta developer: @nobianermodules

from telethon.tl.types import Message
from telethon.tl.functions.channels import EditBannedRequest
from telethon.tl.types import ChatBannedRights
from datetime import timedelta, datetime, timezone
from .. import loader, utils
import re

@loader.tds
class ModerationMod(loader.Module):
    """Модуль для модерації чатів"""

    strings = {
        "name": "Moderation",
        "ban_success": "🚫 Користувач {user} був заблокований на {duration}.",
        "unban_success": "✅ Користувач {user} розблокований.",
        "mute_success": "🔇 Користувач {user} обеззвучений на {duration}.",
        "unmute_success": "🔊 Користувач {user} може знову надсилати повідомлення.",
        "warn_success": "⚠️ Користувачу {user} видано попередження. ({warn_count}/{warn_limit})",
        "unwarn_success": "⚠️ Всі попередження з користувача {user} зняті.",
        "no_user": "❌ Не вдалося знайти користувача. Використайте @username або реплай на повідомлення користувача.",
        "warn_limit_reached": "🚫 Користувач {user} отримав {warn_limit} попереджень та був покараний. Попередження користувача зкинуті.",
        "warn_limit_set": "✅ Ліміт попереджень встановлено на {limit}.",
        "warnpunish_enabled": "✅ Покарання за попередження активовано.",
        "warnpunish_disabled": "❌ Покарання за попередження деактивовано.",
        "warnpunish_status": "🔄 Покарання за поперердження наразі: {status}.",
        "punishment_set": "✅ Покарання за поперердження встановлено на {punishment}.",
        "invalid_punishment": "❌ Невірний аргумент. Використайте 'mute' або 'ban'.",
        "punishment_duration_set": "✅ Покарання {punishment} встановлено на {duration}.",
        "invalid_duration": "❌ Невірний формат тривалості. Використайте щось накшталт: 1d, 2h, 3m, 4s",
        "welcome_msg_set": "✅ Привітальне повідомлення встановлено.",
        "goodbye_msg_set": "✅ Прощальне повідомлення встановлено.",
        "welcome_enabled": "✅ Привітання нових користувачів активовано.",
        "welcome_disabled": "❌ Привітання нових користувачів деактивовано.",
        "goodbye_enabled": "✅ Прощання активовано.",
        "goodbye_disabled": "❌ Прощання деактивовано.",
        "welcome": "👋 Ласкаво просимо, {user}!",
        "goodbye": "👋 Прощавай, {user}!",
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "warn_limit",
                3,
                "Ліміт попереджень"
            ),
            loader.ConfigValue(
                "warn_punish",
                True,
                "Активувати або деактивувати покарання за досягнення ліміту попереджень"
            ),
            loader.ConfigValue(
                "punishment_type",
                "ban",
                "Тип покарання за досягнення ліміту попереджень (ban або mute)"
            ),
            loader.ConfigValue(
                "punishment_duration",
                None,
                "Тривалість покарання (None - назавжди)"
            ),
            loader.ConfigValue(
                "welcome_enabled",
                False,
                "Активувати або деактивувати привітання нових користувачів"
            ),
            loader.ConfigValue(
                "goodbye_enabled",
                False,
                "Активувати або деактивувати прощавальні повідомлення"
            ),
            loader.ConfigValue(
                "welcome_msg",
                "👋 Ласкаво просимо, {user}!",
                "Привітальне повідомлення"
            ),
            loader.ConfigValue(
                "goodbye_msg",
                "👋 Прощавай, {user}!",
                "Прощавальне повідомлення"
            ),
        )
        self.warnings = {}  

    @property
    def warn_limit(self):
        return self.config["warn_limit"]

    @property
    def warn_punish(self):
        return self.config["warn_punish"]

    @property
    def punishment_type(self):
        return self.config["punishment_type"]
    
    @property
    def punishment_duration(self):
        return self.config["punishment_duration"]
    
    @property
    def welcome_enabled(self):
        return self.config["welcome_enabled"]

    @property
    def goodbye_enabled(self):
        return self.config["goodbye_enabled"]

    @property
    def welcome_msg(self):
        return self.config["welcome_msg"]

    @property
    def goodbye_msg(self):
        return self.config["goodbye_msg"]

    def parse_duration(self, duration_str):
        """Парсинг тривалості покарання (1d, 1h, та ін.)"""
        match = re.match(r"(\d+)([smhd])", duration_str)
        if match:
            duration_value = int(match.group(1))
            duration_unit = match.group(2)
            if duration_unit == 's':
                return timedelta(seconds=duration_value)
            elif duration_unit == 'm':
                return timedelta(minutes=duration_value)
            elif duration_unit == 'h':
                return timedelta(hours=duration_value)
            elif duration_unit == 'd':
                return timedelta(days=duration_value)
        return None

    async def get_user(self, message: Message, args):
        if message.is_reply:
            reply = await message.get_reply_message()
            return await self.client.get_entity(reply.sender_id)
        elif args:
            return await self.client.get_entity(args)
        else:
            return None
        
    async def user_joined(self, event):
        """Обробляє вступ нових користувачів та надсилає привітальне повідомлення"""
        if not self.welcome_enabled:
            return
        await event.reply(self.welcome_msg.format(user=event.user.first_name))

    async def user_left(self, event):
        """Обробляє вихід користувачів з чату та надсилає прощавальне повідомлення"""
        if not self.goodbye_enabled:
            return
        await event.reply(self.goodbye_msg.format(user=event.user.first_name))

    async def watcher(self, event):
        """Відслідковування вступу та виходу користувачів"""
        if event.user_joined:
            await self.user_joined(event)
        elif event.user_left:
            await self.user_left(event)
    
    async def welcomecmd(self, message: Message):
       """Активувати або деактивувати привітання нових користувачів"""
       self.config["welcome_enabled"] = not self.welcome_enabled
       status = "активовані" if self.welcome_enabled else "деактивовані"
       await utils.answer(message, f"✅ Привітальні повідомлення {status}.")

    async def goodbyecmd(self, message: Message):
       """Активувати або деактивувати прощавальні повідомлення"""
       self.config["goodbye_enabled"] = not self.goodbye_enabled
       status = "активовані" if self.goodbye_enabled else "деактивовані"
       await utils.answer(message, f"✅ Прощавальні повідомлення {status}.")

    
    async def setwelcomemsgcmd(self, message: Message):
        """Встановити привітальне повідомлення"""
        args = utils.get_args_raw(message)
        if not args:
            return await utils.answer(message, "❌ Вкажіть текст для повідомлення.")
        self.config["welcome_msg"] = args
        await utils.answer(message, self.strings["welcome_msg_set"])

    async def setgoodbyemsgcmd(self, message: Message):
        """Встановити прощавальне повідомлення"""
        args = utils.get_args_raw(message)
        if not args:
            return await utils.answer(message, "❌ Вкажіть текст для повідомлення.")
        self.config["goodbye_msg"] = args
        await utils.answer(message, self.strings["goodbye_msg_set"])

    async def bancmd(self, message: Message):
        """Заблоувати користувача в чаті"""
        args = utils.get_args_raw(message).split()

        if message.is_reply:
            user = await self.get_user(message, "")
            duration = self.parse_duration(args[0]) if len(args) == 1 else None
        else:
            if len(args) == 0:
                return await utils.answer(message, self.strings["no_user"])
            duration = self.parse_duration(args[1]) if len(args) == 2 else None
            user = await self.get_user(message, args[0])

        if not user:
            return await utils.answer(message, self.strings["no_user"])

        until_date = datetime.now(timezone.utc) + duration if duration else None
        duration_str = args[1] if len(args) == 2 else args[0] if duration else "назавжди"

        ban_rights = ChatBannedRights(until_date=until_date, view_messages=True)

        await self.client(EditBannedRequest(message.chat_id, user.id, ban_rights))
        await utils.answer(message, self.strings["ban_success"].format(user=user.first_name, duration=duration_str))

    async def mutecmd(self, message: Message):
        """Обеззвучити користувача в чаті"""
        args = utils.get_args_raw(message).split()

        if message.is_reply:
            user = await self.get_user(message, "")
            duration = self.parse_duration(args[0]) if len(args) == 1 else None
        else:
            if len(args) == 0:
                return await utils.answer(message, self.strings["no_user"])
            duration = self.parse_duration(args[1]) if len(args) == 2 else None
            user = await self.get_user(message, args[0])

        if not user:
            return await utils.answer(message, self.strings["no_user"])

        until_date = datetime.now(timezone.utc) + duration if duration else None
        duration_str = args[1] if len(args) == 2 else args[0] if duration else "назавжди"

        mute_rights = ChatBannedRights(until_date=until_date, send_messages=True)

        await self.client(EditBannedRequest(message.chat_id, user.id, mute_rights))
        await utils.answer(message, self.strings["mute_success"].format(user=user.first_name, duration=duration_str))

    async def unmutecmd(self, message: Message):
        """Надати можливість говорити користувачу в чаті"""
        args = utils.get_args_raw(message).split()
        user = await self.get_user(message, args[0] if args else "")
        if not user:
            return await utils.answer(message, self.strings["no_user"])

        unmute_rights = ChatBannedRights(until_date=None, send_messages=False)

        await self.client(EditBannedRequest(message.chat_id, user.id, unmute_rights))
        await utils.answer(message, self.strings["unmute_success"].format(user=user.first_name))

    async def warncmd(self, message: Message):
        """Видати попередження користувачу"""
        args = utils.get_args_raw(message).split()
        user = await self.get_user(message, args[0] if not message.is_reply else "")

        if not user:
            return await utils.answer(message, self.strings["no_user"])

        user_id = user.id
        if user_id not in self.warnings:
            self.warnings[user_id] = 0
        self.warnings[user_id] += 1

        if self.warnings[user_id] >= self.warn_limit and self.warn_punish:
            punishment = self.punishment_type
            until_date = datetime.now(timezone.utc) + self.punishment_duration if self.punishment_duration else None

            if punishment == "ban":
                ban_rights = ChatBannedRights(until_date=until_date, view_messages=True)
                await self.client(EditBannedRequest(message.chat_id, user.id, ban_rights))
            elif punishment == "mute":
                mute_rights = ChatBannedRights(until_date=until_date, send_messages=True)
                await self.client(EditBannedRequest(message.chat_id, user.id, mute_rights))

            self.warnings[user_id] = 0  
            await utils.answer(message, self.strings["warn_limit_reached"].format(user=user.first_name, warn_limit=self.warn_limit))
        else:
            await utils.answer(message, self.strings["warn_success"].format(user=user.first_name, warn_count=self.warnings[user_id], warn_limit=self.warn_limit))

    async def unwarncmd(self, message: Message):
        """Зняти всі попередження з користувача"""
        args = utils.get_args_raw(message).split()
        user = await self.get_user(message, args[0] if not message.is_reply else "")

        if not user:
            return await utils.answer(message, self.strings["no_user"])

        user_id = user.id
        self.warnings[user_id] = 0  
        await utils.answer(message, self.strings["unwarn_success"].format(user=user.first_name))

    async def warnlistcmd(self, message: Message):
        """Посмотреть количество предупреждений пользователя"""
        args = utils.get_args_raw(message).split()
        user = await self.get_user(message, args[0] if not message.is_reply else "")

        if not user:
            return await utils.answer(message, self.strings["no_user"])

        user_id = user.id
        warn_count = self.warnings.get(user_id, 0)  

        await utils.answer(message, f"⚠️ У користувача {user.first_name} {warn_count} попереджень.") 

    async def setwarncountcmd(self, message: Message):
        """Встановити ліміт попереджень для покарання"""
        args = utils.get_args_raw(message).split()
        if not args or not args[0].isdigit():
            return await utils.answer(message, "❌ Будь-ласка, вкажіть коректне число.")

        limit = int(args[0])
        self.config["warn_limit"] = limit  
        await utils.answer(message, self.strings["warn_limit_set"].format(limit=limit))

    async def setwarnpunishcmd(self, message: Message):
        """
        Встановити покарання за досягнення ліміту попереджень
        """
        args = utils.get_args_raw(message).split()

        if len(args) == 0:
            return await utils.answer(message, self.strings["invalid_punishment"])

        punishment = args[0].lower()
        if punishment not in ["mute", "ban"]:
            return await utils.answer(message, self.strings["invalid_punishment"])

        if len(args) == 2:
            duration = self.parse_duration(args[1])
            if not duration:
                return await utils.answer(message, self.strings["invalid_duration"])
            self.config["punishment_duration"] = duration
            await utils.answer(message, self.strings["punishment_duration_set"].format(punishment=punishment, duration=args[1]))
        else:
            self.config["punishment_duration"] = None
            await utils.answer(message, self.strings["punishment_set"].format(punishment=punishment))

        self.config["punishment_type"] = punishment

    async def warnpunishcmd(self, message: Message):
        """Активувати/деактивувати покарання за досягнення ліміту попереджень"""
        current_status = self.warn_punish
        new_status = not current_status
        self.config["warn_punish"] = new_status

        if new_status:
            await utils.answer(message, self.strings["warnpunish_enabled"])
        else:
            await utils.answer(message, self.strings["warnpunish_disabled"])
