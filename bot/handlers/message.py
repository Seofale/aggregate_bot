import json

from aiogram import Router
from aiogram.types import Message

from bot.utils import get_group_salary_data


router = Router(name="message-router")


@router.message()
async def message_callback(message: Message, json_text: dict):
    response = await get_group_salary_data(
        dt_from_iso=json_text["dt_from"],
        dt_upto_iso=json_text["dt_upto"],
        group_type=json_text["group_type"],
    )
    await message.answer(json.dumps(response))
