from aiogram import Router, types
from database import (
get_user,
already_paid,
add_tax
)

from utils import (
check_tax_message,
get_amount,
get_week,
get_month,
get_moscow_time
)

router = Router()

@router.message()
async def tax_check(message: types.Message):

text = message.text or ""

# Проверяем, похоже ли сообщение на сдачу налога
if not check_tax_message(text):
    return


nickname = None

# Если сообщение переслано от пользователя
if message.forward_from:
    nickname = (
        message.forward_from.username
        or str(message.forward_from.id)
    )

# Если нет информации о пересылке
if not nickname:
    await message.answer(
        "❌ Не удалось определить игрока."
    )
    return


# Проверяем наличие в клане
user = await get_user(nickname)

if not user:
    await message.answer(
        "❌ Вас нет в списке участников клана."
    )
    return


# Проверяем повторную сдачу
if await already_paid(nickname):

    await message.answer(
        "⚠️ Налог уже был засчитан за эту неделю."
    )
    return


amount = get_amount(text)


await add_tax(
    nickname,
    user[1],
    amount,
    str(get_moscow_time()),
    get_week(),
    get_month()
)


await message.answer(
    "✅ Налог принят!\n\n"
    f"👤 Игрок: {nickname}\n"
    f"💰 Сумма: {amount} золота"
)