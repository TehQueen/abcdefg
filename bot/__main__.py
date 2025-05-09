import asyncio

from bot.core import bot, db_handler, dp, scheduler
from bot.handlers import routers


async def main():
    """
    Main entry point for the bot application.
    This asynchronous function performs the following tasks:
    1. Initializes the database handler.
    2. Includes routers into the dispatcher if they are provided as a list or tuple.
    3. Deletes the bot's webhook and optionally drops pending updates.
    4. Starts polling for updates using the bot and dispatcher.
    Raises:
        Exception: If any error occurs during the execution of the tasks.
    """
    assert await db_handler.init()

    if routers and isinstance(routers, (list, tuple)):
        dp.include_routers(*routers)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
