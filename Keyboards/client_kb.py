from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


#-----main menu

start_bt = KeyboardButton('/start')
contacts_bt = KeyboardButton('/contacts')
check_list__bt = KeyboardButton('/checklist')

client_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
client_keyboard.row(start_bt, contacts_bt, check_list__bt)





