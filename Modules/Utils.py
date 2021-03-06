from datetime import datetime
from os import environ

from aiogram.dispatcher.filters import CommandStart
from aiogram.types import Message
from humanize import i18n, precisedelta

from bot import dp
from Misc import create_backup

i18n.activate("pt_BR")


@dp.message_handler(CommandStart())
async def _start(m: Message) -> None:
    txt = (
        f"Olá {m.from_user.first_name}!\n"
        f"Eu sou um bot com multi-funções. "
        f"Para saber mais sobre mim, digite /help.\n"
    )

    return await m.answer(txt)


@dp.message_handler(commands=["uptime", "up"])
async def _uptime(m: Message) -> None:
    uptime = datetime.now() - dp.utils["uptime"]
    return await m.answer(f"Meu uptime: {precisedelta(uptime, format='%0.0f')}")


@dp.message_handler(commands=["backup"])
async def _backup(m: Message) -> None:
    if m.from_user.id == int(environ["OWNER_ID"]):
        txt = await create_backup(datetime.now(), m.bot)
        return await m.answer(txt)
    return await m.answer("Você não tem permissão para executar esse comando !")


@dp.message_handler(commands=["help"])
async def _help(m: Message) -> None:
    txt = (
        f"Olá {m.from_user.first_name}!\n"
        f"Esses são alguns dos comandos que eu possuo:\n"
        f"/start - Comando de inicio.\n"
        f"/help - Mostra os comandos.\n"
        f"/uptime - Mostra o uptime do bot.\n"
    )
    return await m.answer(txt)
