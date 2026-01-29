import os

import aiosqlite
import dotenv
from aiogram import Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import User, Message

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
            await bot.send_message(user.id, "Вы уже регистрировались в базе! Отмена!")
            return

    await state.set_state(ABP.fcs)
    await bot.send_message(user.id, "Отправь своё ФИО полностью")


async def write_to_database(data: dict, user: User):
    async with aiosqlite.connect(os.getenv("DATABASE_NAME")) as db:
        await db.execute(
            request_text,
            (user.id, user.username, data["fcs"], data["city"], data["school"], data["phone"])
        )
        await db.commit()


async def stop_fsm(message: Message, state: FSMContext, bot: Bot):
    data = await state.get_data()
    await write_to_database(data, message.from_user)

    try:
        await bot.approve_chat_join_request(int(os.getenv("CHAT_ID")), message.from_user.id)
    except:
        pass

    await state.set_state(None)
    await bot.send_message(int(os.getenv("ADMIN_CHAT_ID")),
                           f"Новый запрос\n\nФИО: {data["fcs"]}\nГород: {data["city"]}\nШкола: {data["school"]}\nНомер телефона: {data["phone"]}")
    await bot.send_contact(
        int(os.getenv("ADMIN_CHAT_ID")),
        first_name=data["fcs"],
        last_name=f"{data["city"]} {data["school"]}",
        phone_number=data["phone"]
    )
