"""
    This module contains methods of Inline Telegram Keyboard
"""
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def prepare_keyboard(data):
    """
        That function prepares data for keyboard
    """
    keyboard = InlineKeyboardMarkup(row_width=1)
    buttons = []
    for title, url in data.items():
        buttons.append(InlineKeyboardButton(title, callback_data=url))
    keyboard.add(*buttons)
    return keyboard
