"""
This module initializes and configures the core components of the bot, including:
- Logging: Configures the logging system to display messages with a specific format and level.
- Database Handler: Initializes the database handler for interacting with the database using the DSN from the settings.
- Scheduler: Sets up an asynchronous scheduler with a specified timezone for scheduling tasks.
- Bot: Creates an instance of the bot with the provided token and default properties, such as parse mode and link preview settings.
- Dispatcher: Initializes the dispatcher with in-memory storage for handling bot updates and state management.
Modules and Libraries Used:
- aiogram: For bot and dispatcher functionalities.
- apscheduler: For scheduling tasks asynchronously.
- logging: For logging configuration.
- bot.database: Custom module for database handling.
- bot.core.config: Custom module for accessing configuration settings.
"""
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from bot.database import DatabaseHandler
from bot.core.config import settings

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
