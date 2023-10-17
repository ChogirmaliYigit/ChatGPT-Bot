from aiogram.dispatcher.filters.state import State, StatesGroup


class ChatState(StatesGroup):
    content = State()
    repost = State()