import os

from aiogram import Router, Bot
from aiogram.types import CallbackQuery, Message
import dotenv
import aiosqlite

from states import AcceptRequest

callback_query_router = Router()

dotenv.load_dotenv()

ADMIN_CHAT = int(os.getenv("ADMIN_CHAT_ID"))
CHAT = int(os.getenv("CHAT_ID"))
DATABASE_NAME = os.getenv("DATABASE_NAME")


@callback_query_router.callback_query(AcceptRequest.filter())
async def accept_request_callback_query_router(callback_query: CallbackQuery, bot: Bot):
    if callback_query.message.chat.id != ADMIN_CHAT:
        return

    callback_data = AcceptRequest.unpack(callback_query.data)

    if callback_data.accept:
        try:
            await bot.approve_chat_join_request(CHAT, callback_data.user_id)
        except:
            pass

    else:
        async with aiosqlite.connect(DATABASE_NAME) as db:
            await db.execute(
                "DELETE FROM users WHERE telegram_id = ?",
                (callback_data.user_id,))
            await db.commit()

    await callback_query.message.edit_reply_markup(reply_markup=None)
    try:
        await bot.decline_chat_join_request(CHAT, callback_data.user_id)
        await bot.send_message(callback_data.user_id,
                               "Ваша заявка была отклонена. Возможно вы ввели невалидные данные. Попробуйте еще раз")
    except:
        pass
