# meta developer: @nobianermodules
import requests
from bs4 import BeautifulSoup
from telethon.tl.functions.account import UpdateProfileRequest
from .. import loader, utils
import asyncio

@loader.tds
class SteamStatusMod(loader.Module):
    """
    Модуль для взаємодії з Steam.
    """

    strings = {
        "name": "SteamStatus",
        "no_profile_link": "🚫 Посилання на профіль не встановлено. Використайте команду .linkprofile <ссылка>.",
        "profile_link_set": "🔗 Посилання на профіль встановлено: {}",
        "bio_set": "📝 Поле 'Про себе' буде автоматично оновлюватися.",
        "playing_game": "🎮 Грає в: {}",
        "not_playing": "🚫 Не грає.",
        "error": "❌ Помилка при отриманні даних про користувача Steam.",
        "profile_info": "<emoji document_id=5373144051690258848>📱</emoji> Профіль користувача: {}\n\n<emoji document_id=5373012449597335010>👤</emoji> Нікнейм: {}\n<emoji document_id=5463054218459884779>🌡</emoji> Рівень: {}\n<emoji document_id=5467583879948803288>🎮</emoji> Статус: {}\n<emoji document_id=5361741454685256344>🎮</emoji> Ігор: {}\n<emoji document_id=5372926953978341366>👥</emoji> Друзів: {}\n<emoji document_id=5451646226975955576>⌛️</emoji> Остання активність за 2 тижні: {} год.",
        "proflink_info": "<emoji document_id=5373144051690258848>📱</emoji> Профіль користувача: {}\n\n<emoji document_id=5373012449597335010>👤</emoji> Нікнейм: {}\n<emoji document_id=5463054218459884779>🌡</emoji> Рівень: {}\n<emoji document_id=5467583879948803288>🎮</emoji> Статус: {}\n<emoji document_id=5361741454685256344>🎮</emoji> Ігор: {}\n<emoji document_id=5372926953978341366>👥</emoji> Друзів: {}\n<emoji document_id=5451646226975955576>⌛️</emoji> Остання активність за 2 тижні: {} год."
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "profile_link",
                None,
                "Посилання на ваш Steam профіль"
            ),
            loader.ConfigValue(
                "update_interval",
                60,
                "Інтервал оновлення статуса (в секундах)"
            ),
            loader.ConfigValue(
                "auto_update_bio",
                False,
                "Автоматично оновлювати поле 'Про себе'"
            )
        )

    async def client_ready(self, client, db):
        self.client = client
        self.db = db
        self._check_task = self.client.loop.create_task(self._check_steam_status())

    async def linkprofilecmd(self, message):
        """- .linkprofile <посилання> - Встановлює посилання на ваш Steam профіль."""
        args = utils.get_args_raw(message)
        if not args:
            await utils.answer(message, self.strings["no_profile_link"])
            return

        self.config["profile_link"] = args.strip()
        await utils.answer(message, self.strings["profile_link_set"].format(args.strip()))

    async def profilecmd(self, message):
        """- .profile - Показує інформацію про ваш Steam профіль."""
        if not self.config["profile_link"]:
            await utils.answer(message, self.strings["no_profile_link"])
            return

        profile_data = self._get_steam_profile_data(self.config["profile_link"])
        if profile_data:
            await utils.answer(message, self.strings["profile_info"].format(
                self.config["profile_link"],
                profile_data.get('nickname', 'Невідомо'),
                profile_data.get('level', 'Невідомо'),
                profile_data.get('status', 'Не грає'),
                profile_data.get('games', 'Невідомо'),
                profile_data.get('friends', 'Невідомо'),
                profile_data.get('recent_activity', 'Невідомо')
            ))
        else:
            await utils.answer(message, self.strings["error"])

    async def proflinkcmd(self, message):
        """- .proflink <посилання> - Показує інформацію про будь-який Steam профіль."""
        args = utils.get_args_raw(message)
        if not args:
            await utils.answer(message, "🚫 Вкажіть посилання на профіль Steam.")
            return

        profile_data = self._get_steam_profile_data(args.strip())
        if profile_data:
            await utils.answer(message, self.strings["proflink_info"].format(
                args.strip(),
                profile_data.get('nickname', 'Невідомо'),
                profile_data.get('level', 'Невідомо'),
                profile_data.get('status', 'Не грає'),
                profile_data.get('games', 'Невідомо'),
                profile_data.get('friends', 'Невідомо'),
                profile_data.get('recent_activity', 'Невідомо')
            ))
        else:
            await utils.answer(message, self.strings["error"])

    async def setbiocmd(self, message):
        """- .setbio - Вмикає та вимикає автоматичне оновлення вашого Steam статусу в полі 'Про себе'."""
        self.config["auto_update_bio"] = not self.config["auto_update_bio"]
        if self.config["auto_update_bio"]:
            await utils.answer(message, self.strings["bio_set"])
        else:
            await utils.answer(message, "📝 Автоматичне оновлення поля 'Про себе' вимкнено.")

    async def _check_steam_status(self):
        """Функція для перевірки статусу профіля Steam."""
        while True:
            if not self.config["profile_link"]:
                await asyncio.sleep(self.config["update_interval"])
                continue
            
            profile_data = self._get_steam_profile_data(self.config["profile_link"])
            if profile_data:
                current_status = profile_data.get('status', 'Не грає')
                
                if self.config["auto_update_bio"]:
                    await self._update_bio(current_status)
                
                if current_status != "Не грає":
                    print(self.strings["playing_game"].format(current_status))
                else:
                    print(self.strings["not_playing"])
            
            await asyncio.sleep(self.config["update_interval"])

    async def _update_bio(self, status):
        """Оновлює поле 'Про себе' в профилі Telegram в залежності від статуса Steam."""
        try:
            if status != "Не грає":
                bio = f"🎮 Статус Steam: Грає в {status}"
            else:
                bio = "Не грає"

            await self.client(UpdateProfileRequest(about=bio))
        except Exception as e:
            print(f"Поилка при оновленні поля 'Про себе': {e}")

    def _get_steam_profile_data(self, profile_link):
        """Функція для парсингу сторінки профілю Steam і отримання інформації про користувача."""
        try:
            response = requests.get(profile_link)
            if response.status_code != 200:
                print(f"Ошибка доступа к странице: {response.status_code}")
                return None

            soup = BeautifulSoup(response.text, 'html.parser')

            # Поиск никнейма пользователя
            nickname_tag = soup.find("span", class_="actual_persona_name")
            nickname = nickname_tag.text.strip() if nickname_tag else "Невідомо"

            # Поиск уровня пользователя
            level_tag = soup.find("span", class_="friendPlayerLevelNum")
            level = level_tag.text.strip() if level_tag else "Невідомо"

            # Поиск информации о текущей игре
            playing_game = soup.find("div", class_="profile_in_game_header")
            game_info = soup.find("div", class_="profile_in_game_name")

            status = game_info.text.strip() if playing_game and game_info else "Не грає"
            
            games_tag = soup.find("a", {"href": f"{profile_link}games/?tab=all"})
            games = games_tag.find("span", {"class": "profile_count_link_total"}).text.strip() if games_tag else "Невідомо"

            friends_tag = soup.find("div", {"class": "profile_friend_links profile_count_link_preview_ctn responsive_groupfriends_element"})
            friends = friends_tag.find("span", {"class": "profile_count_link_total"}).text.strip() if friends_tag else "Невідомо"

            recent_activity_tag = soup.find("div", {"class": "recentgame_recentplaytime"})
            recent_activity = recent_activity_tag.text.strip().split(' ')[0] if recent_activity_tag else "0"

            return {
                "nickname": nickname,
                "level": level,
                "status": status,
                "games": games,
                "recent_activity": recent_activity,
                "friends": friends
            }

        except Exception as e:
            print(f"Помилка при парсингу сторінки: {e}")
            return None