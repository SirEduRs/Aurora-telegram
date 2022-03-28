import logging
from datetime import datetime
from os import environ

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from dotenv import load_dotenv
from pytz import timezone

from Misc import create_backup

LOG = logging.getLogger("aiogram")


async def create_loop(bot: Bot):
    date = datetime.now().replace(tzinfo=timezone('America/Sao_Paulo'))
    LOG.warning(f'[{date}] Iniciando o backup do servidor...')
    await create_backup(date, bot)


load_dotenv(".env")

bot: Bot = Bot(token=environ.get("BOT_TOKEN"))
dp: Dispatcher = Dispatcher(bot, storage=MemoryStorage())

dp.utils = dict()
dp.utils["uptime"] = datetime.now()

sched = AsyncIOScheduler(timezone=timezone('America/Sao_Paulo'))
LOG.warning('Iniciando o scheduler...')
sched.add_job(create_loop, 'cron', hour=0, minute=0, args=[bot])
sched.start()

from Modules import Utils
