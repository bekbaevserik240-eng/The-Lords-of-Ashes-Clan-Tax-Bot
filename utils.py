import re
from datetime import datetime
import pytz

from config import TAX_KEYWORDS, TIMEZONE

def get_moscow_time():
tz = pytz.timezone(TIMEZONE)
return datetime.now(tz)

def get_week():
now = get_moscow_time()
return now.strftime("%Y-%W")

def get_month():
now = get_moscow_time()
return now.strftime("%Y-%m")

def check_tax_message(text: str):
"""
Проверяет сообщение игры
"""

for keyword in TAX_KEYWORDS:
    if keyword.lower() in text.lower():
        return True

return False

def get_amount(text: str):
"""
Ищет количество золота в сообщении
Например:
"Ты успешно положил в казну 💰 250 золотых"
"""

result = re.search(r"(\d+)\s*золот", text)

if result:
    return int(result.group(1))

return 0

def format_user(nickname, amount, date):
return (
f"👤 Игрок: {nickname}\n"
f"💰 Сумма: {amount} золота\n"
f"📅 Дата: {date}"
)

def format_list(users):
if not users:
return "Список пуст."

text = "👥 Участники клана:\n\n"

for user in users:
    text += f"• {user[2]}\n"

return text