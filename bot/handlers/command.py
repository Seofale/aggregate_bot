import json
from pathlib import Path
from datetime import datetime

from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from bot.bot import CustomBot


command_router = Router()


@command_router.message(Command(commands=["start"]))
async def start_handler(message: Message):
    return await message.answer(
        f"Hello, {message.from_user.username}!"
    )


@command_router.message(Command(commands=["example"]))
async def example_handler(message: Message):
    return await message.answer(
        """
        Запрос:
            /aggregate {
                "dt_from": "2022-09-01T00:00:00",
                "dt_upto": "2022-12-31T23:59:00",
                "group_type": "month",
                "date_field_name": "dt",
                "value_field_name": "value"
            }
        Ответ:
            {"dataset": [5906586, 5515874, 5889803, 6092634],
            "labels": ["2022-09-01T00:00:00", "2022-10-01T00:00:00",
                    "2022-11-01T00:00:00", "2022-12-01T00:00:00"]}
        """
    )


@command_router.message(Command(commands=["aggregate"]))
async def message_handler(message: Message, bot: CustomBot, command: Command):
    data = json.loads(command.args)
    response = await bot.mongo.get_group_salary_data(
        tg_id=message.from_user.id,
        dt_from_iso=data["dt_from"],
        dt_upto_iso=data["dt_upto"],
        group_type=data["group_type"],
        date_field_name=data["date_field_name"],
        value_field_name=data["value_field_name"],
    )
    return await message.answer(json.dumps(response))


@command_router.message(
    Command(commands=["import"]),
)
async def import_handler(message: Message, bot: CustomBot):
    document = message.document
    if not (document or document.file_name.endswith(".json")):
        return await message.answer(
            "You should pin json file using this command"
        )

    folder_name = Path(__file__).parents[1].joinpath("data")
    filename = f"{folder_name}/{datetime.now()}|{document.file_name}"
    await message.answer(
        "Пожалуйста, подождите, пока данные импортируются"
    )
    await bot.download(
        file=document,
        destination=filename,
    )
    await bot.mongo.import_json_data(
        tg_id=message.from_user.id,
        chat_id=message.chat.id,
        filename=filename,
    )
    await message.answer(
        "Данные импортированы"
    )
