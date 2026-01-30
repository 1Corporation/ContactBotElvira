import os
from html import escape

import aiosqlite
import dotenv
from aiogram import Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import User, Message
from aiogram.utils.keyboard import InlineKeyboardMarkup, InlineKeyboardButton

from states.callback_data import AcceptRequest
from states.states_groups import ABP

dotenv.load_dotenv()
request_text = """
               INSERT INTO users
               VALUES (?, ?, ?, ?, ?, ?) \
               """


async def start_fsm(user: User, state: FSMContext, bot: Bot):
    async with aiosqlite.connect(os.getenv("DATABASE_NAME")) as db:
        query = await db.execute(
            "SELECT * FROM users WHERE telegram_id = ?", (user.id,)
        )

        if await query.fetchone() is not None:
            await bot.send_message(user.id, "Ты уже отправлял запрос на вступление в группу и либо находишься в ней, либо твоя заявка еще рассматривается. Жди когда она будет рассмотрена")
            return

    await state.set_state(ABP.fcs)
    await bot.send_message(user.id, """Привет!👋

Я бот-помощник учебного центра №1.
Моя задача, защитить вашу беседу от вредного спама, дабы вас не тревожили мошенники!

Предлагаю познакомиться, надеюсь ты согласен❤️

Но используй реальные данные, а то я могу отклонить твою заявку на вступление в беседу

И так, сначала скажи, пожалуйста, своё ФИО:""")


async def write_to_database(data: dict, user: User):
    async with aiosqlite.connect(os.getenv("DATABASE_NAME")) as db:
        await db.execute(
            request_text,
            (user.id, user.username, data["fcs"], data["city"], data["school"], None)
        )
        await db.commit()


async def stop_fsm(message: Message, state: FSMContext, bot: Bot):
    data = await state.get_data()
    await write_to_database(data, message.from_user)
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[[
            InlineKeyboardButton(text="Принять",
                                 callback_data=AcceptRequest(
                                     accept=True,
                                     user_id=message.from_user.id).pack()
                                 ),
            InlineKeyboardButton(
                text="Отклонить",
                callback_data=AcceptRequest(
                    accept=False,
                    user_id=message.from_user.id
                ).pack()
            )
        ]]
    )
    await state.set_state(None)
    text = (
        "Новый запрос\n\n"
        f"Имя в телеграмм: {escape(message.from_user.full_name)}\n"
        f"Юзернейм: @{escape(message.from_user.username)}\n"
        f"ФИО: {escape(data['fcs'])}\n"
        f"Город: {escape(data['city'])}\n"
        f"Школа: {escape(data['school'])}\n"
        f"Payload для добавления в контакты: <code>copy {escape(data['fcs'])} {escape(data['city'])} {escape(data['school'])}</code>"
    )
    await bot.send_message(int(os.getenv("ADMIN_CHAT_ID")),
                           text, reply_markup=keyboard,
                           parse_mode="HTML")
    # await bot.send_contact(
    #     int(os.getenv("ADMIN_CHAT_ID")),
    #     first_name=data["fcs"],
    #     last_name=f"{data["city"]} {data["school"]}",
    #     phone_number=data["phone"],
    #     reply_markup=keyboard
    # )
