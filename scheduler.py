from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
import pytz

from config import TIMEZONE
from database import get_users, get_user, reset_week

scheduler = AsyncIOScheduler(
timezone=pytz.timezone(TIMEZONE)
)

async def send_notify(bot):
users = await get_users()

for user in users:
    telegram_id = user[1]

    try:
        await bot.send_message(
            telegram_id,
            "🔔 Напоминание!\n\n"
            "Сегодня нужно пополнить казну клана."
        )

    except Exception:
        pass

async def reset_tax(bot):
users = await get_users()

for user in users:
    telegram_id = user[1]

    try:
        await bot.send_message(
            telegram_id,
            "🔄 Новый налоговый период начался!\n"
            "Не забудьте пополнить казну клана в пятницу."
        )

    except Exception:
        pass

await reset_week()

def start_scheduler(bot):

scheduler.add_job(
    lambda: send_notify(bot),
    CronTrigger(
        day_of_week="fri",
        hour=18,
        minute=0
    )
)

scheduler.add_job(
    lambda: send_notify(bot),
    CronTrigger(
        day_of_week="fri",
        hour=22,
        minute=0
    )
)

scheduler.add_job(
    lambda: reset_tax(bot),
    CronTrigger(
        day_of_week="fri",
        hour=23,
        minute=59
    )
)

scheduler.start()