from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline.callback_datas import send_document_callback

template_achievement_keyboard = InlineKeyboardMarkup()

b1 = InlineKeyboardButton(text='Показать пример',
                          callback_data=send_document_callback.new(name='template', hide=True))

template_achievement_keyboard.add(b1)
