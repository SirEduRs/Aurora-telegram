from os import environ

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from dotenv import load_dotenv

load_dotenv("bot.env")

bot: Bot = Bot(token=environ.get("BOT_TOKEN"))
dp: Dispatcher = Dispatcher(bot, storage=MemoryStorage())

from Modules import Utils
