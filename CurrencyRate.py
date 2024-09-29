# meta developer: @nobianermodules
from .. import loader
import requests

@loader.tds
class CurrencyRateMod(loader.Module):
    """Показує поточний курс валюти"""

    strings = {"name": "CurrencyRate"}

    async def ratecmd(self, message):
        """Отримати курс валюти"""
        try:
            response = requests.get("https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?json")
            response.raise_for_status()
            data = response.json()

            usd_rate = next((item for item in data if item["cc"] == "USD"), None)
            eur_rate = next((item for item in data if item["cc"] == "EUR"), None)

            if usd_rate and eur_rate:
                usd_to_uah = usd_rate["rate"]
                eur_to_uah = eur_rate["rate"]
                result = (f"💰 Курс валюти:\n\n"
                          f"💵 1 USD = {usd_to_uah} UAH\n"
                          f"💶 1 EUR = {eur_to_uah} UAH")
            else:
                result = "Не вдалося отримати дані щодо курсу"
        except requests.exceptions.RequestException as e:
            result = f"Помилка: {e}"

        await message.edit(result)
