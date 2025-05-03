import asyncio

from create_bot import bot, dp, scheduler
from handlers import routers


async def main():
    dp.include_routers(*routers)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
