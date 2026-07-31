from aiogram import Router, types
from aiogram.filters import Command

from config import ADMIN_ID
from database import (
add_user,
remove_user,
get_users,
reset_week
)

router = Router()

def is_admin(user_id):
return user_id == ADMIN_ID

@router.message(Command("add"))
async def add_player(message: types.Message):

if not is_admin(message.from_user.id):
    return

args = message.text.split(maxsplit=1)

if len(args) < 2:
    await message.answer(
        "Использование:\n/add Ник"
    )
    return

nickname = args[1]

await add_user(
    message.from_user.id,
    nickname
)

await message.answer(
    f"✅ Игрок {nickname} добавлен в клан."
)

@router.message(Command("addlist"))
async def add_list(message: types.Message):

if not is_admin(message.from_user.id):
    return

text = message.text.replace(
    "/addlist",
    ""
).strip()

if not text:
    await message.answer(
        "После команды укажите ники каждый с новой строки."
    )
    return


count = 0

for nickname in text.split("\n"):

    nickname = nickname.strip()

    if nickname:
        await add_user(
            0,
            nickname
        )
        count += 1


await message.answer(
    f"✅ Добавлено игроков: {count}"
)

@router.message(Command("remove"))
async def remove_player(message: types.Message):

if not is_admin(message.from_user.id):
    return

args = message.text.split(maxsplit=1)

if len(args) < 2:
    await message.answer(
        "Использование:\n/remove Ник"
    )
    return

nickname = args[1]

await remove_user(nickname)

await message.answer(
    f"🗑 Игрок {nickname} удален."
)

@router.message(Command("reset"))
async def reset(message: types.Message):

if not is_admin(message.from_user.id):
    return

await reset_week()

await message.answer(
    "🔄 Налоговая неделя сброшена."
)

@router.message(Command("notify"))
async def notify(message: types.Message):

if not is_admin(message.from_user.id):
    return

users = await get_users()

count = 0

for user in users:

    await message.bot.send_message(
        user[1],
        "🔔 Напоминание!\n\n"
        "Не забудьте сдать налог в казну клана."
    )

    count += 1


await message.answer(
    f"📢 Напоминания отправлены: {count}"
)