import logging

from aiogram import Dispatcher

from .error import ErrorMiddleware


logger = logging.getLogger("middlewares")


def setup_middlewares(dp: Dispatcher):
    dp.message.middleware(ErrorMiddleware(logger))
