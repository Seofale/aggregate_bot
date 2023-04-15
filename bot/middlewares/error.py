import json
import logging
from typing import Callable, Awaitable, Dict, Any

from aiogram import BaseMiddleware
from aiogram.types import Message, TelegramObject


class ErrorMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any],
    ) -> Any:
        try:
            json_text = json.loads(event.text)
            data["json_text"] = json_text
            await handler(event, data)
        except json.JSONDecodeError:
            await event.answer("Incorrect JSON format")
        except Exception as e:
            logging.error(str(e))
            await event.answer("Incorrect JSON data")
