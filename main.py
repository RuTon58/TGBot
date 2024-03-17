# Імпортуємо необхідні інструменти
import logging, sys, asyncio
from data import TOKENS
from Classes import Database

from aiogram import Bot, Dispatcher
from routers import client_router
from data.create_database import create_database

# Вказуємо класу бази даних шлях до файлу БД та створюємо таблиці у БД
db = Database("data/sqlite_database.db")
create_database(db)
# Створюємо екземпляр бота та діспетчера для обробки подій
bot = Bot(token=TOKENS["BOT"])
dp = Dispatcher()
# Підключаємо роутер клієнта до діспетчера 
dp.include_router(client_router)

# Створюємо функцію запуску бота
async def start_bot():
    await dp.start_polling(bot)
     
# Запускаємо бота
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(start_bot())
