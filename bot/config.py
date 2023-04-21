from pydantic import BaseSettings
from aiogram import Bot


class Settings(BaseSettings):
    bot_token: str
    mongo_host: str
    mongo_port: int
    mongo_db: str
    mongo_db_col: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()


def setup_config(bot: Bot):
    bot.config = settings
