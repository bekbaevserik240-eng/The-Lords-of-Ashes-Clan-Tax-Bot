from aiogram import Router, types
from aiogram.filters import Command

from config import ADMIN_ID
from database import get_users
from config import DATABASE

import aiosqlite

router = Router()

def is_admin(user_id):
return user_id == ADMIN_ID

@router.message(Command("report"))
async def report(message: types.Message):

if not is_admin(message.from_user.id):
    return

async with aiosqlite.connect(DATABASE) as db:

    cursor = await db.execute(
        """
        SELECT nickname, amount
        FROM current_tax
        """
    )

    paid = await cursor.fetchall()


users = await get_users()

text = "📊 Отчет за текущую неделю\n\n"

text += "✅ Сдали:\n"

if paid:
    for player in paid:
        text += (
            f"• {player[0]} — "
            f"{player[1]} золота\n"
        )
else:
    text += "Нет\n"


text += "\n❌ Не сдали:\n"

for user in users:

    found = False

    for player in paid:
        if player[0] == user[2]:
            found = True

    if not found:
        text += f"• {user[2]}\n"


await message.answer(text)

@router.message(Command("week"))
async def week(message: types.Message):

if not is_admin(message.from_user.id):
    return


async with aiosqlite.connect(DATABASE) as db:

    cursor = await db.execute(
        """
        SELECT nickname, amount, week
        FROM weekly_history
        ORDER BY id DESC
        LIMIT 30
        """
    )

    data = await cursor.fetchall()


text = "📅 История пятниц:\n\n"

if not data:
    text += "Истории пока нет."

else:

    for row in data:

        text += (
            f"👤 {row[0]}\n"
            f"💰 {row[1]} золота\n"
            f"📅 {row[2]}\n\n"
        )


await message.answer(text)

@router.message(Command("month"))
async def month(message: types.Message):

async with aiosqlite.connect(DATABASE) as db:

    cursor = await db.execute(
        """
        SELECT nickname,
               SUM(amount)
        FROM taxes
        GROUP BY nickname
        ORDER BY SUM(amount) DESC
        """
    )

    data = await cursor.fetchall()


text = "📊 Статистика месяца:\n\n"

if not data:
    text += "Данных нет."

else:

    place = 1

    for row in data:

        text += (
            f"{place}. {row[0]} — "
            f"{row[1]} золота\n"
        )

        place += 1


await message.answer(text)