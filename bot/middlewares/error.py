import logging
from typing import Callable, Awaitable, Dict, Any

from aiogram import BaseMiddleware
from aiogram.types import Message, TelegramObject


class ErrorMiddleware(BaseMiddleware):
    def __init__(self, logger: logging.Logger):
        super().__init__()
        self.logger = logger

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any],
    ) -> Any:
        try:
            await handler(event, data)
        except Exception as e:
            self.logger.exception(str(e))
            await event.answer("Похоже, вы допустили ошибку при запросе :(")
