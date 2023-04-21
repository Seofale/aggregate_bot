from aiogram import Bot
from bot.config import Settings
from bot.store import Mongo


class CustomBot(Bot):
    config: Settings | None = None
    mongo: Mongo | None = None
