from aiogram.filters.callback_data import CallbackData



class AcceptRequest(CallbackData, prefix="accept_request"):
    accept: bool
    user_id: int
