# ---------------------------------------------------------------------------------
#  /\_/\  🌐 This module was loaded through https://t.me/hikkamods_bot
# ( o.o )  🔐 Licensed under the Copyleft license.
#  > ^ <   ⚠️ Owner of heta.hikariatama.ru doesn't take any responsibilities or intellectual property rights regarding this script
# ---------------------------------------------------------------------------------
# Name: accounttime
# Author: vsecoder
# Commands:
# .actime
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

__version__ = (2, 5, 0)

import asyncio
import logging
import time
from datetime import datetime
from typing import Callable, Tuple

import numpy as np
from dateutil.relativedelta import relativedelta

from .. import loader, utils

data = {
    "5396587273": 1648014800,
    "5336336790": 1646368100,
    "4317845111": 1620028800,
    "3318845111": 1618028800,
    "2018845111": 1608028800,
    "1919230638": 1598028800,
    "755000000": 1548028800,
    "782000000": 1546300800,
    "727572658": 1543708800,
    "616816630": 1529625600,
    "391882013": 1509926400,
    "400169472": 1499904000,
    "369669043": 1492214400,
    "234480941": 1464825600,
    "200000000": 1451606400,
    "150000000": 1434326400,
    "10000000": 1413331200,
    "7679610": 1389744000,
    "2768409": 1383264000,
    "1000000": 1380326400,
}


class Function:
    def __init__(self, order: int = 3):
        self.order = 3

        self.x, self.y = self._unpack_data()
        self._func = self._fit_data()

    def _unpack_data(self) -> Tuple[list, list]:
        x_data = np.array(list(map(int, data.keys())))
        y_data = np.array(list(data.values()))

        return (x_data, y_data)

    def _fit_data(self) -> Callable[[int], int]:
        fitted = np.polyfit(self.x, self.y, self.order)
        return np.poly1d(fitted)

    def add_datapoint(self, pair: tuple):
        pair[0] = str(pair[0])

        data.update([pair])

        # update the model with new data
        # self.x, self.y = self._unpack_data()
        self._func = self._fit_data()

    def func(self, tg_id: int) -> int:
        value = self._func(tg_id)
        current = time.time()

        if value > current:
            value = current

        return value


logger = logging.getLogger(__name__)


@loader.tds
class AcTimeMod(loader.Module):
    """Модуль для отримання дати створення аккаунта"""

    strings = {
        "name": "Account Time",
        "info": "Get the account registration date and time!",
        "error": "Error!",
    }

    strings_ua = {
        "info": "Дізнайся дату реєстрації акаунта, і час, який ви його використовуєте!",
        "error": "Помилка!",
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            "answer_text",
            (
                "⏳ Цей акаунт: {0}\n🕰 Створено: {1}\n\nP.S. Скрипт модуля"
                " тренувався на кількості запитів з різних ідентифікаторів, тому дані"
                " тому він буде допрацьовуватися"
            ),
            lambda m: self.strings("cfg_answer_text", m),
        )
        self.name = self.strings["name"]

    async def client_ready(self, client, db):
        self.client = client
        self.db = db

    def time_format(self, unix_time: int, fmt="%Y-%m-%d") -> str:
        result = [str(datetime.utcfromtimestamp(unix_time).strftime(fmt))]

        d = relativedelta(datetime.now(), datetime.utcfromtimestamp(unix_time))
        result.append(f"{d.years} years, {d.months} months, {d.days} days")

        return result

    @loader.unrestricted
    @loader.ratelimit
    async def actimecmd(self, message):
        """
         - отримати дату і час реєстрації облікового запису [бета-версія].
        P.S. Ви також можете відправити команду у відповідь на повідомлення
        """
        try:
            interpolation = Function()
            reply = await message.get_reply_message()

            if reply:
                date = self.time_format(
                    unix_time=round(interpolation.func(int(reply.sender.id)))
                )
            else:
                date = self.time_format(
                    unix_time=round(interpolation.func(int(message.from_id)))
                )

            await utils.answer(
                message, self.config["answer_text"].format(date[0], date[1])
            )
        except Exception as e:
            await utils.answer(message, f'{self.strings["error"]}\n\n{e}')
            if message.out:
                await asyncio.sleep(5)
                await message.delete()
