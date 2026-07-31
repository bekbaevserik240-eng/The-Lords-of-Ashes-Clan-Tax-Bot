import aiosqlite
from config import DATABASE

async def init_db():
async with aiosqlite.connect(DATABASE) as db:
await db.execute("""
CREATE TABLE IF NOT EXISTS users (
id INTEGER PRIMARY KEY AUTOINCREMENT,
telegram_id INTEGER,
nickname TEXT UNIQUE,
username TEXT,
active INTEGER DEFAULT 1
)
""")

    await db.execute("""
    CREATE TABLE IF NOT EXISTS taxes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nickname TEXT,
        telegram_id INTEGER,
        amount INTEGER,
        date TEXT,
        week TEXT,
        month TEXT
    )
    """)

    await db.execute("""
    CREATE TABLE IF NOT EXISTS current_tax (
        nickname TEXT PRIMARY KEY,
        telegram_id INTEGER,
        amount INTEGER,
        date TEXT
    )
    """)

    await db.execute("""
    CREATE TABLE IF NOT EXISTS weekly_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nickname TEXT,
        amount INTEGER,
        week TEXT,
        date TEXT
    )
    """)

    await db.execute("""
    CREATE TABLE IF NOT EXISTS monthly_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nickname TEXT,
        amount INTEGER,
        month TEXT
    )
    """)

    await db.commit()

Добавление участника

async def add_user(telegram_id, nickname, username=None):
async with aiosqlite.connect(DATABASE) as db:
await db.execute(
"""
INSERT OR IGNORE INTO users
(telegram_id, nickname, username)
VALUES (?, ?, ?)
""",
(telegram_id, nickname, username)
)
await db.commit()

Удаление участника

async def remove_user(nickname):
async with aiosqlite.connect(DATABASE) as db:
await db.execute(
"DELETE FROM users WHERE nickname=?",
(nickname,)
)
await db.commit()

Получить всех участников

async def get_users():
async with aiosqlite.connect(DATABASE) as db:
cursor = await db.execute(
"SELECT * FROM users WHERE active=1"
)
return await cursor.fetchall()

Найти игрока

async def get_user(nickname):
async with aiosqlite.connect(DATABASE) as db:
cursor = await db.execute(
"SELECT * FROM users WHERE nickname=?",
(nickname,)
)
return await cursor.fetchone()

Проверка сдачи

async def already_paid(nickname):
async with aiosqlite.connect(DATABASE) as db:
cursor = await db.execute(
"SELECT * FROM current_tax WHERE nickname=?",
(nickname,)
)
return await cursor.fetchone()

Записать налог

async def add_tax(nickname, telegram_id, amount, date, week, month):
async with aiosqlite.connect(DATABASE) as db:
await db.execute(
"""
INSERT INTO current_tax
VALUES (?, ?, ?, ?)
""",
(nickname, telegram_id, amount, date)
)

    await db.execute(
        """
        INSERT INTO taxes
        VALUES (NULL, ?, ?, ?, ?, ?, ?)
        """,
        (nickname, telegram_id, amount, date, week, month)
    )

    await db.commit()

Получить сдавших

async def get_paid():
async with aiosqlite.connect(DATABASE) as db:
cursor = await db.execute(
"SELECT * FROM current_tax"
)
return await cursor.fetchall()

Очистить текущую неделю

async def reset_week():
async with aiosqlite.connect(DATABASE) as db:
await db.execute(
"DELETE FROM current_tax"
)
await db.commit()