import sqlite3
from BotCreator import bot
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton


def sql_start():
    global base, cursor
    base = sqlite3.connect('Users.db')
    cursor = base.cursor()
    if base:
        print('Data base connected!')
        base.execute(
            "CREATE TABLE IF NOT EXISTS messages(img TEXT, message TEXT PRIMARY KEY)")
        base.execute(
            "CREATE TABLE IF NOT EXISTS users_for_mailing(user_id INT PRIMARY KEY, status TEXT)")
        base.commit()


async def sql_add_commands(state):
    async with state.proxy() as data:
            cursor.execute("INSERT INTO messages VALUES (?,?)", tuple(data.values()))
            base.commit()


async def sql_read(answer: Message):
    for i in cursor.execute("SELECT * FROM messages").fetchall():
        await bot.send_photo(answer.from_user.id, i[0], f'Message: {i[1]}',
                             reply_markup=InlineKeyboardMarkup().add(
                                 InlineKeyboardButton(text='broadcast ✉️', callback_data=f"done {i[1]}")))


async def sql_read_as_list():
    return cursor.execute('SELECT * FROM messages').fetchall()


async def sql_deleter(item):
    cursor.execute('DELETE FROM messages WHERE message == ?', (item,))
    base.commit()


# here we are starting with mailing db
async def add_user_for_mailing(user_id):
    status = 'waiting'
    cursor.execute("INSERT OR IGNORE INTO users_for_mailing (user_id, status) VALUES (?, ?)", (user_id, status))
    base.commit()


async def read_users_as_list():
    return cursor.execute('SELECT * FROM users_for_mailing').fetchall()



