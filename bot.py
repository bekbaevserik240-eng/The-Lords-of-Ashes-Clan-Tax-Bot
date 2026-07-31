import asyncio

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode

from config import BOT_TOKEN

from database import init_db

from scheduler import start_scheduler

from handlers import (
admin,
user,
tax,
statistics
)

async def main():

bot = Bot(
    token=BOT_TOKEN,
    parse_mode=ParseMode.HTML
)

dp = Dispatcher()


# Подключаем обработчики

dp.include_router(
    admin.router
)

dp.include_router(
    statistics.router
)

dp.include_router(
    user.router
)

dp.include_router(
    tax.router
)


# Создаем базу

await init_db()


# Запускаем расписание

start_scheduler(bot)


print(
    "🤖 Бот запущен"
)


await dp.start_polling(bot)

if name == "main":

asyncio.run(main())