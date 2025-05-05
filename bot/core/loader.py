import os
import logging

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from .. import middlewares


scheduler = AsyncIOScheduler(timezone='Europe/Moscow')

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

bot = Bot(token=os.environ.get('BOT_TOKEN'),
          default=DefaultBotProperties(parse_mode=ParseMode.HTML,
                                       link_preview_is_disabled=True))
dp = Dispatcher(storage=MemoryStorage())

[
    dp.message.outer_middleware.register(middleware)
        for middleware in middlewares.__middlewares__
]
