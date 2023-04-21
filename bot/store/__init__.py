from bot.store.database import Mongo
from aiogram import Bot


def setup_database(bot: Bot):
    bot.mongo = Mongo(bot)
