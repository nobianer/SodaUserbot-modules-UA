# meta developer: @nobianermodules, @SodaModules
import asyncio
import requests
import time
from bs4 import BeautifulSoup
from telethon.tl.functions.account import UpdateProfileRequest
from .. import loader, utils
import io

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
        "error": "❌ Помилка при отриманні даних про користувача Steam.",
        "profile_info": "<emoji document_id=5373144051690258848>📱</emoji> Профіль користувача: {}\n\n<emoji document_id=5373012449597335010>👤</emoji> Нікнейм: {}\n<emoji document_id=5463054218459884779>🌡</emoji> Рівень: {}\n<emoji document_id=5467583879948803288>🎮</emoji> Статус: {}\n<emoji document_id=5361741454685256344>🎮</emoji> Ігор: {}\n<emoji document_id=5372926953978341366>👥</emoji> Друзів: {}\n<emoji document_id=5451646226975955576>⌛️</emoji> Остання активність за 2 тижні: {} год."
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
        self.previous_status = None

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
        """- .profile - Показує інформацію про ваш Steam профіль та робить скриншот."""
        if not self.config["profile_link"]:
            await utils.answer(message, self.strings["no_profile_link"])
            return

        profile_data = self._get_steam_profile_data(self.config["profile_link"])
        if profile_data:
            screenshot = self._get_screenshot(self.config["profile_link"])

            if screenshot:
                profile_text = self.strings["profile_info"].format(
                    self.config["profile_link"],
                    profile_data.get('nickname', 'Невідомо'),
                    profile_data.get('level', 'Невідомо'),
                    profile_data.get('status', 'Не грає'),
                    profile_data.get('games', 'Невідомо'),
                    profile_data.get('friends', 'Невідомо'),
                    profile_data.get('recent_activity', 'Невідомо')
                )

                await message.client.send_file(
                    message.chat_id,
                    screenshot,
                    caption=profile_text
                )
                await message.delete()
            else:
                await utils.answer(message, self.strings["error"])
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
            await utils.answer(message, self.strings["profile_info"].format(
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

    async def _check_steam_status(self):
        """Перевірка статусу"""
        while True:
            if not self.config["profile_link"]:
                await asyncio.sleep(self.config["update_interval"])
                continue
            
            profile_data = self._get_steam_profile_data(self.config["profile_link"])
            if profile_data:
                current_status = profile_data.get('status', 'Не грає')

                if self.config["auto_update_bio"] and current_status != self.previous_status:
                    await self._update_bio(current_status)
                    self.previous_status = current_status
            
            await asyncio.sleep(self.config["update_interval"])
            
    async def setbiocmd(self, message):
        """- .setbio - Вмикає та вимикає автоматичне оновлення вашого Steam статусу в полі 'Про себе'."""
        self.config["auto_update_bio"] = not self.config["auto_update_bio"]
        if self.config["auto_update_bio"]:
            await utils.answer(message, self.strings["bio_set"])
        else:
            await utils.answer(message, "📝 Автоматичне оновлення поля 'Про себе' вимкнено.")

    async def _update_bio(self, status):
        """Оновлення біо"""
        try:
            if status == "Онлайн":
                bio = "🟢 Статус Steam: Онлайн"
            elif status == "Офлайн":
                bio = "🔴 Статус Steam: Офлайн"
            elif status != "Не грає":
                bio = f"🎮 Статус Steam: Грає в {status}"
            else:
                bio = "Не грає"

            await self.client(UpdateProfileRequest(about=bio))
            
        except Exception as e:
            print(f"Помилка при оновлені поля 'Про себе': {e}")

    def _get_steam_profile_data(self, profile_link):
        """Функція для парсингу сторінки профілю Steam і отримання інформації про користувача."""
        try:
            response = requests.get(profile_link)
            if response.status_code != 200:
                print(f"Помилка доступу до сторінки: {response.status_code}")
                return None

            soup = BeautifulSoup(response.text, 'html.parser')

            nickname_tag = soup.find("span", class_="actual_persona_name")
            if nickname_tag:
                nickname = nickname_tag.text.strip()
            else:
                print("Помилка: нікнейм не знайдено.")
                nickname = "Невідомо"

            level_tag = soup.find("span", class_="friendPlayerLevelNum")
            if level_tag:
                level = level_tag.text.strip()
            else:
                print("Помилка: рівень не знайдено.")
                level = "Невідомо"

            status_tag = soup.find("div", class_="profile_in_game")
            if status_tag:
                status_class = status_tag.get("class", "")
                if "in-game" in status_class:
                    status = soup.find("div", class_="profile_in_game_name").text.strip()
                elif "online" in status_class:
                    status = "Онлайн"
                elif "offline" in status_class:
                    status = "Офлайн"
                else:
                    status = "Невідомий статус"
            else:
                print("Помилка: Статус не найден.")
                status = "Невідомий статус"

            games_tag = soup.find("a", {"href": f"{profile_link}games/?tab=all"})
            if games_tag:
                games = games_tag.find("span", {"class": "profile_count_link_total"}).text.strip()
            else:
                print("Помилка: ігри не знайдено.")
                games = "Невідомо"

            friends_tag = soup.find("div", {"class": "profile_friend_links profile_count_link_preview_ctn responsive_groupfriends_element"})
            if friends_tag:
                friends = friends_tag.find("span", {"class": "profile_count_link_total"}).text.strip()
            else:
                print("Помилка: друзі не знайдені.")
                friends = "Невідомо"

            recent_activity_tag = soup.find("div", {"class": "recentgame_recentplaytime"})
            if recent_activity_tag:
                recent_activity = recent_activity_tag.text.strip().split(' ')[0]
            else:
                print("Помилка: остання активність не знайдена.")
                recent_activity = "0"

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

    def _get_screenshot(self, url):
        """Робить скріншот за допомогою API."""
        api_url = f"https://api.apiflash.com/v1/urltoimage"
        params = {
            "access_key": "api_key",
            "url": url,
            "width": "1920",
            "height": "1304",
            "format": "png",
            "fresh": "true",
            "accept_language": "uk",
            "crop": "0,104,1920,1200",
            "wait_until": "page_loaded"
        }

        try:
            response = requests.get(api_url, params=params, stream=True)
            if response.status_code == 200:
                timestamp = int(time.time())
                screenshot = io.BytesIO(response.content)
                screenshot.name = f"steam_profile_{timestamp}.png"
                return screenshot
            else:
                print(f"Помилка під час створення скріншота: {response.status_code}")
                return None
        except Exception as e:
            print(f"Помилка під час створення скріншота {e}")
            return None
