from aiogram import Dispatcher

from .message import message_router


def setup_routers(dp: Dispatcher):
    dp.include_router(message_router)
