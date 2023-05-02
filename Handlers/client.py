from aiogram import types, Dispatcher
from BotCreator import bot
from Keyboards.client_kb import client_keyboard
from DataBase import sqlite_db


redirection = """<b><i>U can communicate with bot only in private messages
                 Please, text him</i></b>\n
                 <b>https://t.me/user_send_bot</b>
                 """


async def command_start(answer: types.Message):
    try:
        await bot.send_message(answer.from_user.id, f'Greetings!', reply_markup=client_keyboard)
        await answer.delete()
        await sqlite_db.add_user_for_mailing(answer.from_user.id)
    except:
        await answer.reply(redirection)


async def command_contacts(answer: types.Message):
    try:
        await bot.send_message(answer.from_user.id, '<b>Vinnytsia, Street Murі 9</b>')
        await answer.delete()
    except:
        await answer.reply(redirection)


async def message_list(answer: types.Message):
    try:
        await bot.send_message(answer.from_user.id, 'Messages!')
        await answer.delete()
        await sqlite_db.sql_read(answer)
    except:
        await answer.reply(redirection)


def reg_handlers(dp: Dispatcher):
    dp.register_message_handler(command_start, commands=['start'])
    dp.register_message_handler(command_contacts, commands=['contacts'])
    dp.register_message_handler(message_list, commands=['checklist'])