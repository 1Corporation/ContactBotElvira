import os

import asyncio
import aiogram
import dotenv
from aiogram import Dispatcher

from routers import command_router, states_router, join_request_router
from database import create_tables

dotenv.load_dotenv()


bot = aiogram.Bot(token=os.getenv("BOT_TOKEN"))
dp = Dispatcher()


dp.include_router(command_router)
dp.include_router(states_router)
dp.include_router(join_request_router)


def main():
    asyncio.run(create_tables())
    dp.run_polling(bot)


if __name__ == '__main__':
    main()