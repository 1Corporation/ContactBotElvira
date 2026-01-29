import os

import dotenv
from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, BufferedInputFile

from states import manage_states
from utils import build_ping_text, xlsx_dump

command_router = Router()


dotenv.load_dotenv()


ADMIN_CHAT_ID = os.getenv("ADMIN_CHAT_ID")


@command_router.message(CommandStart())
async def start_command(message: Message, state: FSMContext):
    print(message.chat.id)
    if message.chat.id != message.from_user.id:
        return

    await manage_states.start_fsm(message.from_user, state, message.bot)


@command_router.message(Command("ping"))
async def ping_command(message: Message):
    await message.answer(build_ping_text(message.from_user))


@command_router.message(Command("dump_excel"))
async def dump_excel(message: Message):

    if message.chat.id != int(ADMIN_CHAT_ID):
        return

    xlsx = await xlsx_dump()
    xlsx.name = "report.xlsx"
    xlsx.seek(0)
    await message.answer_document(document=BufferedInputFile(xlsx.read(), "report.xlsx"))
