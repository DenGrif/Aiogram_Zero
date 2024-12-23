from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import KeyboardBuilder, InlineKeyboardBuilder

main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Тестовая кнопа - 1")],
    [KeyboardButton(text="Тестовая кнопка - 2"), KeyboardButton(text="Тестовая кнопка - 3")]
], resize_keyboard=True)

inline_keyboard_test = InlineKeyboardMarkup(inline_keyboard=[
   [InlineKeyboardButton(text="Перейти на YouTube", url='https://www.youtube.com/watch?v=HfaIcB4Ogxk')]
])

test = ["кнопка 1", "кнопка 2", "кнопка 3", "кнопка 4"]