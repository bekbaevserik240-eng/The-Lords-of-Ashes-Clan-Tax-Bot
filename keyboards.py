from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def main_keyboard():
return ReplyKeyboardMarkup(
keyboard=[
[
KeyboardButton(text="📋 Список клана"),
KeyboardButton(text="❌ Должники")
],
[
KeyboardButton(text="📊 Мой статус")
]
],
resize_keyboard=True
)

def admin_keyboard():
return ReplyKeyboardMarkup(
keyboard=[
[
KeyboardButton(text="📋 Список клана"),
KeyboardButton(text="❌ Должники")
],
[
KeyboardButton(text="📊 Отчет"),
KeyboardButton(text="🔔 Напомнить")
],
[
KeyboardButton(text="🔄 Сброс")
]
],
resize_keyboard=True
)