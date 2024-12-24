from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Погода"), KeyboardButton(text="Фото НАСА"), KeyboardButton(text="Породы кошек")]
    ],
    resize_keyboard=True
)
