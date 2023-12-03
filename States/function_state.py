from aiogram.dispatcher.filters.state import StatesGroup, State

class UserState(StatesGroup):
    name = State()

class Userhey(StatesGroup):
    usrname = State()

class sendingState(StatesGroup):
    awaitMsg = State()
    confirmation = State()
    photo = State()

class disableALLCat(StatesGroup):
    step1 = State()