from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def prepare_keyboard(data):
    keyboard = InlineKeyboardMarkup()
    buttons = []
    for title, url in data.items():
        buttons.append(InlineKeyboardButton(title, callback_data=url))
    keyboard.add(*buttons)
    return keyboard