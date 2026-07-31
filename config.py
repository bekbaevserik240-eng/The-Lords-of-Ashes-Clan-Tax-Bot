import os
from dotenv import load_dotenv

load_dotenv()

Токен Telegram-бота

BOT_TOKEN = os.getenv("BOT_TOKEN")

Telegram ID владельца бота (главы клана)

ADMIN_ID = 5824767725

Часовой пояс

TIMEZONE = "Europe/Moscow"

День налога

TAX_DAY = "FRI"

Время напоминаний

FIRST_NOTIFY_HOUR = 18
SECOND_NOTIFY_HOUR = 22

Время автоматического сброса

RESET_HOUR = 23
RESET_MINUTE = 59

Фразы для проверки сдачи налога

TAX_KEYWORDS = [
"Пополнение казны клана",
"Ты успешно положил в казну"
]

Файл базы данных

DATABASE = "clan_tax.db"