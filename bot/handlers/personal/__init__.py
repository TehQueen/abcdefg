"""
This module initializes the `personal` package within the `bot.handlers` module.
It imports the `router` object from the `bot.handlers.personal.message` module
and makes it available as part of the public API of this package.
Exports:
    router (object): The router instance for handling personal messages.
"""
from bot.handlers.personal.messages import router as ms_router
from bot.handlers.personal.callbacks import router as cb_router
from bot.middlewares import IncludeHelper


routers = [
    ms_router,
    cb_router,
]

assert routers @ IncludeHelper(
    lambda module: [
        # Add any middlewares here
        module.AuthorizationMiddleware(),
    ],
)

__all__ = ["routers"]
