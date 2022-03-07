from datetime import datetime
from os import environ

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from dotenv import load_dotenv

load_dotenv(".env")

bot: Bot = Bot(token=environ.get("BOT_TOKEN"))
dp: Dispatcher = Dispatcher(bot, storage=MemoryStorage())

dp.utils = dict()
dp.utils["uptime"] = datetime.now()

from Modules import Utils
