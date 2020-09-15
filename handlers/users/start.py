from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from loader import dp


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    text = [
        f'Привет, <b>{message.from_user.full_name}</b>! 😁',
        'Я - бот для создания достижений в стиле MineCraft',
        '',
        '/create - Создать достижение',
        '/list - Список ваших достижений',
    ]

    await message.answer('\n'.join(text))
