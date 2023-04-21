import asyncio

from aiogram import Dispatcher
from aiogram.enums.parse_mode import ParseMode

from bot.logger import setup_logging
from bot.config import settings, setup_config
from bot.handlers import setup_routers
from bot.middlewares import setup_middlewares
from bot.store import setup_database
from bot.bot import CustomBot


async def main():
    bot = CustomBot(settings.bot_token, parse_mode=ParseMode.HTML)
    setup_config(bot)
    setup_database(bot)
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
