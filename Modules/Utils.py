from aiogram.dispatcher.filters import CommandStart
from aiogram.types import Message

from bot import dp


@dp.message_handler(CommandStart())
async def _start(m: Message):
    txt = (
        f"Olá {m.from_user.first_name}!\n"
        f"Eu sou um bot com multi-funções. "
        f"Para saber mais sobre mim, digite /help.\n"
    )

    await m.answer(txt)
