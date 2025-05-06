"""
This module initializes and exports core components of the bot application.
Imports:
    - settings: Configuration settings for the application.
    - bot: The bot instance used for handling interactions.
    - db_handler: Database handler for managing database operations.
    - dp: Dispatcher for managing bot updates and handlers.
    - scheduler: Scheduler for managing periodic tasks.
Exports:
    - bot: The bot instance.
    - dp: The dispatcher instance.
    - db_handler: The database handler.
    - scheduler: The task scheduler.
    - settings: The application settings.
"""
from bot.core.config import settings
from bot.core.loader import bot, db_handler, dp, scheduler

__all__ = [
    "bot",
    "dp",
    "db_handler",
    "scheduler",
    "settings",
]
