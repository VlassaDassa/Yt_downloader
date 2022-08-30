from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove


kb_remove = ReplyKeyboardRemove
menu_ = KeyboardButton('Меню 💤')
yt = KeyboardButton('YouTube')
choice_service = ReplyKeyboardMarkup(resize_keyboard=True)
choice_service.row(yt, menu_)


txt_file = KeyboardButton('Текстовым файлом 🗎')
one_link = KeyboardButton('Ссылкой ✏')
choice_method_yt = ReplyKeyboardMarkup(resize_keyboard=True)
choice_method_yt.row(txt_file, one_link).add(menu_)


txt = KeyboardButton('Текстовым файлом')
link = KeyboardButton('Ссылкой')
choice_method_tt = ReplyKeyboardMarkup(resize_keyboard=True)
choice_method_tt.row(txt, link).add(menu_)


menu = ReplyKeyboardMarkup(resize_keyboard=True).add(menu_)

q1080 = KeyboardButton('1080p')
q720 = KeyboardButton('720p')
q480 = KeyboardButton('480p')
quality = ReplyKeyboardMarkup(resize_keyboard=True)
quality.row(q1080, q720).row(q480, menu_)

mp3 = KeyboardButton('MP3')
quality_lnk = ReplyKeyboardMarkup(resize_keyboard=True)
quality_lnk.row(q1080, q720, mp3).row(q480, menu_)

