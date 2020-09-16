from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import InputFile, CallbackQuery

from keyboards.inline.callback_datas import send_document_callback
from keyboards.inline.items import items_keyboard, all_items_hide_keyboard, popular_items_hide_keyboard
from keyboards.inline.template import template_achievement_keyboard
from loader import dp
from states import Creation
from image_generation.image_generator import create_all_items_image, delete_image, create_achievement_icon, \
    achievement_path, user_image_path, create_achievement_user_image, get_icons


@dp.message_handler(commands=['create'])
async def create_image(message: types.Message):
    await message.answer('Введите <b>верхний</b> текст', reply_markup=template_achievement_keyboard)

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

    await message.answer('Введите <b>номер</b> иконки\n\nИли <b>отправте</b> свою картинку', reply_markup=items_keyboard)

    await Creation.Icon_number.set()


@dp.message_handler(state=Creation.Icon_number, content_types=['text'])
async def set_icon_number(message: types.Message, state: FSMContext):
    try:
        icon_number = int(message.text)
        print(len(get_icons()) + 1)
        print(icon_number)
        if icon_number <= 0 or icon_number >= len(get_icons()) + 1:
            return
        print(1)
    except ValueError:
        return

    async with state.proxy() as data:
        data['icon_number'] = icon_number

        upper_text = data['upper_text']
        bottom_text = data['bottom_text']

    create_achievement_icon(upper_text, bottom_text, icon_number)
    image = InputFile(achievement_path)
    await message.answer_document(image)
    delete_image(achievement_path)

    await state.reset_state(with_data=False)


@dp.message_handler(state=Creation.Icon_number, content_types=['photo'])
async def set_user_image(message: types.Message, state: FSMContext):
    user_image = message.photo[-1]

    async with state.proxy() as data:
        data['user_image'] = user_image

        upper_text = data['upper_text']
        bottom_text = data['bottom_text']

    await user_image.download(user_image_path)
    create_achievement_user_image(upper_text, bottom_text)
    image = InputFile(achievement_path)
    await message.answer_document(image)
    delete_image(achievement_path)

    await state.reset_state(with_data=False)


@dp.callback_query_handler(send_document_callback.filter(name='template'), state='*')
async def send_document(call: CallbackQuery):
    await call.message.edit_reply_markup()
    document = 'https://raw.githubusercontent.com/TimNekk/mc-achievement-bot/master/image_generation/template.png'
    await call.message.answer_document(document, caption='Пример достижения')


@dp.callback_query_handler(send_document_callback.filter(name='popular_items'), state='*')
async def send_document(call: CallbackQuery, callback_data: dict):
    hide = callback_data.get('hide')
    if hide == 'True':
        await call.message.edit_reply_markup()
    else:
        await call.message.edit_reply_markup(popular_items_hide_keyboard)

    document = 'https://raw.githubusercontent.com/TimNekk/mc-achievement-bot/master/image_generation/popular_items.png'
    await call.message.answer_document(document)


@dp.callback_query_handler(send_document_callback.filter(name='all_items'), state='*')
async def send_document(call: CallbackQuery, callback_data: dict):
    hide = callback_data.get('hide')
    print(hide)
    if hide == 'True':
        await call.message.edit_reply_markup()
    else:
        await call.message.edit_reply_markup(all_items_hide_keyboard)

    document = 'https://raw.githubusercontent.com/TimNekk/mc-achievement-bot/master/image_generation/all_items.png'
    await call.message.answer_document(document)