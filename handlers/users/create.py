from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import InputFile

from loader import dp
from states import Creation
from image_generation.image_generator import create_all_items_image, delete_image, create_achievement

@dp.message_handler(commands=['create'])
async def create_image(message: types.Message):
    image = 'https://raw.githubusercontent.com/TimNekk/mc-achievement-bot/master/image_generation/template.png'
    await message.answer_photo(image, caption='Пример Достижения')

    await message.answer('Введите <b>верхний</b> текст')

    await Creation.Upper_text.set()


@dp.message_handler(state=Creation.Upper_text)
async def set_upper_text(message: types.Message, state: FSMContext):
    upper_text = message.text
    async with state.proxy() as data:
        data['upper_text'] = upper_text

    await message.answer('Введите <b>нижний</b> текст')

    await Creation.Bottom_text.set()


@dp.message_handler(state=Creation.Bottom_text)
async def set_upper_text(message: types.Message, state: FSMContext):
    bottom_text = message.text
    async with state.proxy() as data:
        data['bottom_text'] = bottom_text

    create_all_items_image()
    image = InputFile('image_generation/all_items.png')
    await message.answer_document(image, caption='Введите <b>номер</b> иконки')
    delete_image('image_generation/all_items.png')

    await Creation.Icon_number.set()


@dp.message_handler(state=Creation.Icon_number)
async def set_icon_number(message: types.Message, state: FSMContext):
    icon_number = int(message.text)

    async with state.proxy() as data:
        data['icon_number'] = icon_number

        upper_text = data['upper_text']
        bottom_text = data['bottom_text']

    create_achievement(upper_text, bottom_text, icon_number)
    image = InputFile('image_generation/achievement')
    await message.answer_photo(image)
    delete_image('image_generation/achievement')

    await state.reset_state(with_data=False)