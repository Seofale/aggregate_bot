from aiogram import Dispatcher

from .command import command_router
from .message import message_router


def setup_routers(dp: Dispatcher):
    routers = [command_router, message_router]
    dp.include_routers(*routers)
