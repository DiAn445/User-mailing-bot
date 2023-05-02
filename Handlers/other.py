from aiogram import types, Dispatcher
import string



async def bad_words_filter(answer: types.Message):
    if 'fuck' in {i.lower().translate(str.maketrans('', '', string.punctuation + '@')) for i in answer.text.split(' ')}:
        await answer.reply("don't use bad words here!")
        await answer.delete()


def reg_handlers(dp: Dispatcher):
    dp.register_message_handler(bad_words_filter)
