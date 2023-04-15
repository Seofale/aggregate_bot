from aiogram import Dispatcher

from .error import ErrorMiddleware


def setup_middlewares(dp: Dispatcher):
    dp.message.middleware(ErrorMiddleware())
