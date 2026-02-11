from aiogram.fsm.state import StatesGroup, State


class ABP(StatesGroup):
    fcs = State()
    city = State()
    school = State()
    phone = State()
