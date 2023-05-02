import asyncio
import jinja2
from aiogram.dispatcher import FSMContext
from aiogram import types, Dispatcher
from aiogram.dispatcher.filters.state import StatesGroup, State
from BotCreator import bot, dp
from aiogram.dispatcher.filters import Text
from DataBase import sqlite_db
from Keyboards import admin_kb
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


ID = None


class FSMAdmin(StatesGroup):
    photo = State()
    name = State()
    description = State()
    price = State()


async def if_admin(message: types.Message):
    global ID
    ID = message.from_user.id
    await bot.send_message(message.from_user.id, 'ready to work!', reply_markup=admin_kb.button_case_admin)


async def cancel_state(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        current_state = await state.get_state()
        if current_state is None:
            return
        await state.finish()
        await message.reply('canceled')


async def uploader(message: types.Message):
    if message.from_user.id == ID:
        await FSMAdmin.photo.set()
        await message.reply('upload photo:')


async def upload_photo(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['photo'] = message.photo[0].file_id
        await FSMAdmin.next()
        await message.reply('input message:')


async def input_name(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        if message.text == '/cancel':
            await cancel_state(message, state)
            return
        async with state.proxy() as data:
            data['text'] = message.text
        async with state.proxy() as data:
            await message.reply(str(data))
        await sqlite_db.sql_add_commands(state)
        await state.finish()


async def del_callback_command(callback_query: types.CallbackQuery):
    await sqlite_db.sql_deleter(callback_query.data.replace('del ', ''))
    await callback_query.answer(text=f"{callback_query.data.replace('del ', '')} deleted!", show_alert=True)


async def delete_item(item: types.Message):
    if item.from_user.id == ID:
        read = await sqlite_db.sql_read_as_list()
        if read:
            try:
                for i in read:
                    await bot.send_photo(item.from_user.id, i[0], f'{i[1]}',
                                         reply_markup=InlineKeyboardMarkup().add(
                                             InlineKeyboardButton(text=f"Delete: {i[1]}", callback_data=f"del {i[1]}")))
                await item.delete()
            except:
                pass
        else:
            await bot.send_message(item.from_user.id, 'nothing to delete!')


async def done_callback_command(callback_query: types.CallbackQuery):
    res = [i for i in callback_query.data.replace('done ', '').split(',')]
    read_users = await sqlite_db.read_users_as_list()
    read = await sqlite_db.sql_read_as_list()
    answer = [i for i in read if i[1] == res[0]]
    count_success = 0
    count_fails = 0
    successes = []
    fails = []
    for i in read_users:
        if i[1] == 'waiting' and count_success < 1000:
            try:
                await bot.send_photo(i[0], *answer[0])
                count_success += 1
                successes.append(i[0])
                await asyncio.sleep(.05)
            except Exception:
                count_fails += 1
                fails.append(i[0])
                await asyncio.sleep(.05)
    template = jinja2.Template('''
            <html>
                <head>
                    <title>Mailing report</title>
                    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css">
                </head>
                <body>
                    <div class="container">
                        <div class="card">
                            <div class="card-body">
                                <h1 class="card-title">Mailing report</h1>
                                <p>Successfully sent: {{ count_success }}</p>
                                <p>Failed to send: {{ count_fails }}</p>
                                <h2>List of successfully sent users:</h2>
                                <ul>
                                {% for user in successes %}
                                    <li>{{ user }}</li>
                                {% endfor %}
                                </ul>
                                <h2>List of unsuccessfully submitted users:</h2>
                                <ul>
                                {% for user in fails %}
                                    <li>{{ user }}</li>
                                {% endfor %}
                                </ul>
                            </div>
                        </div>
                    </div>
                </body>
            </html>
        ''')
    html_report = template.render(count_success=count_success, count_fails=count_fails, successes=successes,
                                  fails=fails)
    with open('report.html', 'w') as f:
        f.write(html_report)
    with open('report.html', 'rb') as f:
        await dp.bot.send_document(callback_query.from_user.id, f)


def reg_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(uploader, commands=['upload'], state=None)
    dp.register_message_handler(upload_photo, content_types=['photo'], state=FSMAdmin.photo)
    dp.register_message_handler(input_name, content_types=['text'], state=FSMAdmin.name)
    dp.register_message_handler(cancel_state, commands=['cancel'], state="*")
    dp.register_message_handler(cancel_state, Text(equals='cancel', ignore_case=True), state='*')
    dp.register_message_handler(if_admin, commands=['moderator'], is_chat_admin=True)
    dp.register_message_handler(delete_item, commands=['delete'], is_chat_admin=True)
    dp.register_callback_query_handler(del_callback_command, lambda x: x.data and x.data.startswith('del '))
    dp.register_callback_query_handler(done_callback_command, lambda x: x.data and x.data.startswith('done '))
