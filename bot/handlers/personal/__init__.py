"""
This module initializes the `personal` package within the `bot.handlers` module.
It imports the `router` object from the `bot.handlers.personal.message` module
and makes it available as part of the public API of this package.
Exports:
    router (object): The router instance for handling personal messages.
"""
from bot.handlers.personal.message import router

__all__ = ["router"]
