import asyncio

from .core import bot, dp, scheduler
from .handlers import routers


async def main():
    """
    Main entry point for the bot application.

    This asynchronous function sets up the bot by including routers, 
    removing any existing webhook (if applicable), and starting the 
    polling process to handle updates.

    Steps:
    1. Includes all defined routers into the dispatcher.
    2. Deletes the webhook configuration, ensuring no pending updates 
        are retained.
    3. Starts polling to listen for and process incoming updates.

    Raises:
         Any exceptions raised during the setup or polling process.
    """
    if isinstance(routers, (list, tuple)) and routers:
        dp.include_routers(*routers)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
