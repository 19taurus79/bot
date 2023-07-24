from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def make_row_keyboard(items: list[str]) -> ReplyKeyboardMarkup:
    row = [KeyboardButton(text=item) for item in items]
    return ReplyKeyboardMarkup(keyboard=[row], resize_keyboard=True)


def make_app_keyboard(text, http):
    row = KeyboardButton(text=text, web_app=http)
    return ReplyKeyboardMarkup(keyboard=row, resize_keyboard=True)
