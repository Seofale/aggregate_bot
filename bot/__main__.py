import asyncio

from aiogram import Bot, Dispatcher

from bot.logger import setup_logging
from bot.config import settings
from bot.handlers import setup_routers
from bot.middlewares import setup_middlewares


async def main():
    bot = Bot(settings.bot_token.get_secret_value())
    dp = Dispatcher()
    setup_middlewares(dp)
    setup_routers(dp)
    setup_logging()

    try:
        await dp.start_polling(
            bot,
            allowed_updates=dp.resolve_used_update_types(),
        )
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
