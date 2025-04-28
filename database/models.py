import aiosqlite
from config import DB_PATH

async def add_user(telegram_id, name, age, gender, bio, photo, looking_for):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute('''
            INSERT OR REPLACE INTO users (telegram_id, name, age, gender, bio, photo, looking_for)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (telegram_id, name, age, gender, bio, photo, looking_for))
        await db.commit()

async def get_random_user(current_user_id, gender=None, looking_for=None):
    async with aiosqlite.connect(DB_PATH) as db:
        query = 'SELECT * FROM users WHERE telegram_id != ?'
        params = [current_user_id]

        if gender:
            query += ' AND gender = ?'
            params.append(gender)
        
        if looking_for:
            query += ' AND looking_for = ?'
            params.append(looking_for)

        async with db.execute(query, params) as cursor:
            users = await cursor.fetchall()
            return users
