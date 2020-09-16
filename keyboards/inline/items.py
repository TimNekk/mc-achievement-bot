from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline.callback_datas import send_document_callback


b1 = InlineKeyboardButton(text='Популярные иконки 🔥',
                          callback_data=send_document_callback.new(name='popular_items', hide=False))
b2 = InlineKeyboardButton(text='Все иконки',
                          callback_data=send_document_callback.new(name='all_items', hide=False))

items_keyboard = InlineKeyboardMarkup()
items_keyboard.add(b1)
items_keyboard.add(b2)

all_items_keyboard = InlineKeyboardMarkup()
all_items_keyboard.add(b1)

popular_items_keyboard = InlineKeyboardMarkup()
popular_items_keyboard.add(b2)

b3 = InlineKeyboardButton(text='Популярные иконки 🔥',
                          callback_data=send_document_callback.new(name='popular_items', hide=True))
b4 = InlineKeyboardButton(text='Все иконки',
                          callback_data=send_document_callback.new(name='all_items', hide=True))

all_items_hide_keyboard = InlineKeyboardMarkup()
all_items_hide_keyboard.add(b3)

popular_items_hide_keyboard = InlineKeyboardMarkup()
popular_items_hide_keyboard.add(b4)