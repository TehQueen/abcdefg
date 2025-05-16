"""
This module initializes and configures the core components of the bot application.
Modules and Libraries:
- `logging`: Configures logging for the application.
- `aiogram`: Used for bot and dispatcher initialization.
- `apscheduler`: Provides scheduling capabilities for asynchronous tasks.
- `bot.core.config`: Contains application settings.
- `bot.database`: Handles database operations.
Components:
- `db_handler`: A `DatabaseHandler` instance for interacting with the database.
- `scheduler`: An `AsyncIOScheduler` instance for scheduling tasks.
- `locale`: An `I18n` instance for managing internationalization and localization.
- `bot`: A `Bot` instance configured with the bot token and default properties.
- `dp`: A `Dispatcher` instance with in-memory storage for managing bot updates.
Constants:
- `settings`: Configuration settings loaded from `bot.core.config`.
Logging:
- Configured to log messages at the INFO level with a specific format.
Usage:
This module is intended to be imported and used as the core loader for initializing
the bot's components and dependencies.
"""
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.utils.i18n import I18n

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from bot.database import DatabaseHandler
from bot.core.config import settings
from bot.core.logger import LoggingSystem

# Configure logging
LoggingSystem(
    filename=settings.LOG_FILE,
    max_bytes=32*1024*1024,
    buffer_size=24*1024,
    flush_interval=45,
    backup_count=8
)
logger = logging.getLogger(__name__)

# Initialize database handler
db_handler = DatabaseHandler(dsn=settings.DSN)

# Initialize scheduler
scheduler = AsyncIOScheduler(
    timezone=settings.SCHEDULER_TIMEZONE
)

# Initialize i18n (internationalization) for localization
locale = I18n(
    path=settings.LOCALE_DIR,
    default_locale=settings.LOCALE_FALLBACK,
    domain=settings.LOCALE_DOMAIN,
)

# Initialize bot
bot = Bot(
    token=settings.BOT_TOKEN,
    default=DefaultBotProperties(
        parse_mode=ParseMode.HTML,
        link_preview_is_disabled=True,
    ),
)

# Initialize dispatcher
dp = Dispatcher(storage=MemoryStorage())
