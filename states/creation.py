from aiogram.dispatcher.filters.state import StatesGroup, State


class Creation(StatesGroup):
    Upper_text = State()
    Bottom_text = State()
    Icon_number = State()