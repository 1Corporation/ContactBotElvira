from aiogram import Router, Bot, Dispatcher
from aiogram.types import Message, ChatJoinRequest
from aiogram.fsm.context import FSMContext, StorageKey

from states.manage_states import start_fsm

join_request_router = Router()


@join_request_router.chat_join_request()
async def join_request(event: ChatJoinRequest, bot: Bot, dispatcher: Dispatcher):
    await bot.send_message(event.user_chat_id, "Welcome!")

    key = StorageKey(
        bot_id=bot.id,
        chat_id=event.user_chat_id,
        user_id=event.from_user.id,
    )
    state = FSMContext(storage=dispatcher.storage, key=key)
    await start_fsm(event.from_user, state, bot)
