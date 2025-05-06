"""
This module initializes and configures the core components of the bot, including
logging, database handler, scheduler, bot instance, dispatcher, and middlewares.
Modules and Libraries:
- logging: Configures logging for the application.
- aiogram: Provides classes for bot and dispatcher initialization.
- apscheduler: Used for scheduling tasks.
- middlewares: Custom middlewares for the bot.
- database: Handles database interactions.
- config: Contains application settings.
Components:
- Logging: Configured to log messages at the INFO level.
- DatabaseHandler: Initializes the database connection using the DSN from settings.
- AsyncIOScheduler: Scheduler for managing asynchronous tasks, set to the 'Europe/Moscow' timezone.
- Bot: Configures the bot instance with a token from the environment and default properties.
- Dispatcher: Manages bot updates and uses in-memory storage for FSM.
- Middlewares: Registers custom middlewares for processing incoming messages.
Environment Variables:
- BOT_TOKEN: The token for authenticating the bot with Telegram.
Usage:
This module is intended to be imported and used as the core loader for the bot's
components. It ensures all necessary components are initialized and ready for use.
"""
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from .. import middlewares
from ..database import DatabaseHandler
from .config import settings

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize database handler
db_handler = DatabaseHandler(dsn=settings.DSN)

# Initialize scheduler
scheduler = AsyncIOScheduler(timezone='Europe/Moscow')

# Initialize bot
bot = Bot(
    token=settings.BOT_TOKEN,
    default=DefaultBotProperties(
        parse_mode=ParseMode.HTML,
        link_preview_is_disabled=True
    )
)

# Initialize dispatcher
dp = Dispatcher(storage=MemoryStorage())

# Register middlewares
for middleware in middlewares.__middlewares__:
    dp.message.outer_middleware.register(middleware)
