# ---------------------------------------------------------------------------------
#  /\_/\  🌐 This module was loaded through https://t.me/hikkamods_bot
# ( o.o )  🔓 Not licensed.
#  > ^ <   ⚠️ Owner of heta.hikariatama.ru doesn't take any responsibilities or intellectual property rights regarding this script
# ---------------------------------------------------------------------------------
# Name: TempMail
# Description: Временная почта by @blazeftg
# meta developer: @nobianermodules
# Commands:
# .getmail | .lookmail | .readmail
# ---------------------------------------------------------------------------------


import asyncio

import requests

from .. import loader, utils


@loader.tds
class TempMailMod(loader.Module):
    """Тимчасова пошта by @blazeftg"""

    strings = {"name": "TempMail"}

    async def getmailcmd(self, message):
        """.getmail
        Отримати адресу тимчасової пошти
        """
        response = requests.get(
            "https://www.1secmail.com/api/v1/?action=genRandomMailbox"
        )
        await message.edit(
            "Ваша адреса електронної пошти: " + f"<code>{str(response.json()[0])}</code>"
        )

    async def lookmailcmd(self, message):
        """.lookmail <адреса ел. пошти>
        Отримати всі повідомлення на пошті
        """
        user_i = utils.get_args_raw(message)
        output_mess = ""
        filtered = user_i.split("@")
        name = filtered[0]
        domain = ""
        try:
            domain = filtered[1]
        except IndexError:
            output_mess = "Введи адресу пошти"
        response = requests.get(
            "https://www.1secmail.com/api/v1/?action=getMessages&login={name}&domain={domain}"
            .format(name=name, domain=domain)
        )
        if response.json() == []:
            output_mess = "На пошті немає листів або ж ти неправильно ввів її адресу"
        else:
            for i in range(len(response.json())):
                output_mess += (
                    "Лист №"
                    + f"<code>{str(i+1)}</code>"
                    + "\nПовідомлення від: "
                    + f"<code>{str(response.json()[i]['from'])}</code>"
                    + "\nТема: "
                    + f"<code>{str(response.json()[i]['subject'])}</code>"
                    + "\nДата отримання: "
                    + f"<code>{str(response.json()[i]['date'])}</code>"
                    + "\nID листа: "
                    + f"<code>{str(response.json()[i]['id'])}</code>"
                    + "\n\n"
                )
        await message.edit(output_mess)

    async def readmailcmd(self, message):
        """.readmail <адреса ел. пошти> <ID повідомлення>
        Прочитати повідомлення на пошті з конкретним ID
        """
        user_i = utils.get_args_raw(message)
        filtered = user_i.split()
        try:
            email = filtered[0]
            id = filtered[1]
            filtered_email = email.split("@")
            name = filtered_email[0]
            domain = filtered_email[1]
            response = requests.get(
                "https://www.1secmail.com/api/v1/?action=readMessage&login={name}&domain={domain}&id={message_id}"
                .format(name=name, domain=domain, message_id=id)
            )
            await message.edit(
                "Дата отримання: "
                + f"<code>{str(response.json()['date'])}</code>"
                + "\nВід: "
                + f"<code>{str(response.json()['from'])}</code>"
                + "\nТема: "
                + f"<code>{str(response.json()['subject'])}</code>"
                + "\nТекст листа: "
                + str(response.json()["textBody"])
            )
        except:
            await message.edit("Неправильна адреса пошти або ID повідомлення")
