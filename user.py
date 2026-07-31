from aiogram import Router, types
from aiogram.filters import Command

from database import (
get_users,
already_paid
)

router = Router()

@router.message(Command("list"))
async def user_list(message: types.Message):

users = await get_users()

text = "👥 Участники клана:\n\n"

for user in users:

    paid = await already_paid(
        user[2]
    )

    status = "✅" if paid else "❌"

    text += (
        f"{status} {user[2]}\n"
    )


await message.answer(text)

@router.message(Command("debt"))
async def debt_list(message: types.Message):

users = await get_users()

text = "❌ Еще не сдали налог:\n\n"

count = 0

for user in users:

    paid = await already_paid(
        user[2]
    )

    if not paid:
        text += (
            f"• {user[2]}\n"
        )
        count += 1


if count == 0:
    text = "✅ Все участники сдали налог!"


await message.answer(text)

@router.message(Command("status"))
async def status(message: types.Message):

nickname = (
    message.from_user.username
    or str(message.from_user.id)
)


paid = await already_paid(
    nickname
)


if paid:

    await message.answer(
        "✅ Вы уже сдали налог."
    )

else:

    await message.answer(
        "❌ Вы еще не сдавали налог."
    )