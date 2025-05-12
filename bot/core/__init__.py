"""
This module initializes and exports core components of the bot application.
Imports:
    - settings: Configuration settings for the bot.
    - bot: The bot instance.
    - db_handler: Database handler for managing database operations.
    - dp: Dispatcher for handling updates and routing.
    - scheduler: Scheduler for managing periodic tasks.
    - locale: Localization utilities for handling translations.
Exports:
    - bot: The bot instance.
    - db_handler: Database handler.
    - dp: Dispatcher instance.
    - locale: Localization utilities.
    - scheduler: Task scheduler.
    - settings: Configuration settings.
"""
from bot.core.config import settings
from bot.core.loader import bot, db_handler, dp, scheduler, locale

__all__ = [
    "bot",
    "db_handler",
    "dp",
    "locale",
    "scheduler",
    "settings",
]
