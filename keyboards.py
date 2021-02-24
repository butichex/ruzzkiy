from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton



start_single_game_button = KeyboardButton('👤 Одиночная игра')
start_duel_game_button = KeyboardButton('⚔️ Дуэль')
set_settings_button = KeyboardButton('⚙️ Изменить настройки')
main_menu_keyboard = ReplyKeyboardMarkup()
main_menu_keyboard.insert(start_single_game_button).insert(start_duel_game_button).insert(set_settings_button) 



single_game_menu_keybaord = ReplyKeyboardMarkup(resize_keyboard=True) 
quit_single_game_button = KeyboardButton('🚪 Выйти из игры')
single_game_menu_keybaord.add(quit_single_game_button)
