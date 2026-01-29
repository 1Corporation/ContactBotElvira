import os
import dotenv

from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, BufferedInputFile

from utils import build_ping_text, xlsx_dump

command_router = Router()


dotenv.load_dotenv()


ADMIN_CHAT_ID = os.getenv("ADMIN_CHAT_ID")


@command_router.message(CommandStart())
async def start_command(message: Message):
    pass


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
