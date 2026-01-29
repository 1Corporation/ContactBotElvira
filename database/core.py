import aiosqlite
import dotenv
import os


dotenv.load_dotenv()


async def create_tables():
    async with aiosqlite.connect(os.getenv("DATABASE_NAME")) as db:
        await db.executescript(open("database/schema.sql").read())
