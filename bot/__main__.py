import asyncio

from aiogram import Bot, Dispatcher

from bot.logger import setup_logging
from bot.config import settings
from bot.handlers import message
from bot.middlewares.error import ErrorMiddleware


async def main():
    bot = Bot(settings.bot_token.get_secret_value())
    dp = Dispatcher()
    dp.message.middleware(ErrorMiddleware())
    dp.include_router(message.router)
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
