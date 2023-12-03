from aiogram.dispatcher.filters.state import StatesGroup, State

class ProductState(StatesGroup):
    categories = State()
    collection = State()
    name = State()
    photo = State()
    description = State()
    color = State()
    price = State()
    prin = State()