import asyncio

from bot.core import bot, db_handler, dp, locale, scheduler
from bot.handlers import routers
from bot.middlewares import IncludeHelper


async def main():
    """
    The main entry point for the bot application.
    This asynchronous function initializes the database handler, sets up the dispatcher
    with optional middlewares, includes routers if provided, and starts polling for updates.
    Steps performed:
    1. Initializes the database handler and ensures it is ready.
    2. Configures the dispatcher with middlewares, such as throttling.
    3. Includes routers into the dispatcher if a list or tuple of routers is provided.
    4. Deletes the webhook (if any) and drops pending updates to ensure a clean start.
    5. Starts polling for updates using the bot instance.
    Raises:
        AssertionError: If the database handler fails to initialize or if the dispatcher
                        setup fails.
    Note:
        - Ensure that `db_handler` and `dp` are properly initialized before calling this function.
        - The `routers` variable should be a list or tuple of router instances if used.
    """
    
    assert await db_handler.init()
    
    assert dp @ IncludeHelper(
        lambda module: [
            # Add any middlewares here
            module.AdvancedThrottleMiddleware(),
            module.SimpleI18nMiddleware(i18n=locale),
        ],
    )

    if routers and isinstance(routers, (list, tuple)):
        dp.include_routers(*routers)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
