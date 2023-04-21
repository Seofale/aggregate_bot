from aiogram import Router
from aiogram.types import Message


message_router = Router()


@message_router.message()
async def start_handler(message: Message):
    return await message.answer(
        """
        Список доступных команд:
        1) /import - импортирует Ваш json файл с данными \
            (необходимо прикрепить его к сообщению)
        2) /aggregate - аггрегирует Ваши данные
        3) /example - пример запроса и ответа аггрегации
        В документах импортируемой Вами коллекции данных, \
        обязательно должны присутствовать поля даты и значения, \
        именно их Вы укажете при аггрегации данных!
        """
    )
