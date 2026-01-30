from aiogram.filters.callback_data import CallbackData



class AcceptRequest(CallbackData):
    accept: bool
    user_id: int
