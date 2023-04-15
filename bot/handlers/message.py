import json

from aiogram import Router
from aiogram.types import Message
from aiogram.handlers import BaseHandler

from bot.utils import get_group_salary_data


message_router = Router()


@message_router.message()
class MessageHandler(BaseHandler[Message]):
    async def handle(self):
        response = await get_group_salary_data(
            dt_from_iso=self.data["json_text"]["dt_from"],
            dt_upto_iso=self.data["json_text"]["dt_upto"],
            group_type=self.data["json_text"]["group_type"],
        )
        await self.event.answer(json.dumps(response))
