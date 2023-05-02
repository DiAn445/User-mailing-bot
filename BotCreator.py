from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

storage = MemoryStorage()
bot = Bot(token='5951281687:AAFEF73tHD-MdPXN0fudA6Cy_p1xzS1AGLA', parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=storage)