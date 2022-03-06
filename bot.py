import asyncio
from datetime import datetime

from os import environ
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

load_dotenv('bot.env')

bot: Bot = Bot(token=environ.get('BOT_TOKEN'))
dp: Dispatcher = Dispatcher(bot, storage=MemoryStorage())

from Modules import Utils