#meta developer: @nobianermodules
from .. import loader
import requests

@loader.tds
class WikipediaMod(loader.Module):
    """Надає інформацію з Вікіпедії за запитом"""

    strings = {"name": "Wikipedia"}

    async def wikicmd(self, message):
        """Знайти статтю на Вікіпедії"""
        args = message.raw_text.split(maxsplit=1)

        if len(args) < 2:
            await message.edit("Ви не вказали запит!")
            return
        
        query = args[1]
        try:
            response = requests.get(
                "https://uk.wikipedia.org/api/rest_v1/page/summary/" + query
            )
            response.raise_for_status()
            data = response.json()

            if "extract" in data:
                title = data.get("title", "Немає заголовку")
                extract = data["extract"]
                result = f"📚 {title}\n\n{extract}"
            else:
                result = "Не вдалося знайти статтю за вашим запитом."
        except requests.exceptions.RequestException as e:
            result = f"Помилка: {e}"

        await message.edit(result)
