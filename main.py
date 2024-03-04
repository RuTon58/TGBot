import logging, sys, asyncio
from data import TOKENS
from Classes import Database

from aiogram import Bot, Dispatcher
from routers import client_router
from data.create_database import create_database


db = Database("data/sqlite_database.db")
create_database(db)

bot = Bot(token=TOKENS["BOT"])
dp = Dispatcher()

dp.include_router(client_router)


async def start_bot():
    await dp.start_polling(bot)
     

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(start_bot())
