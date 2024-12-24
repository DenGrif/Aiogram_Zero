from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

# Меню с кнопками "Привет" и "Пока"
main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Привет"), KeyboardButton(text="Пока")]
    ],
    resize_keyboard=True
)

# Кнопки с URL-ссылками
links_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Новости", url="https://ya.ru/")],
        [InlineKeyboardButton(text="Музыка", url="https://music.yandex.ru")],
        [InlineKeyboardButton(text="Видео", url="https://video.yandex.ru")]
    ]
)

# Динамическая клавиатура
def dynamic_keyboard():
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text="Показать больше", callback_data="show_more"))
    return keyboard.as_markup()

def expanded_keyboard():
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text="Опция 1", callback_data="option_1"))
    keyboard.add(InlineKeyboardButton(text="Опция 2", callback_data="option_2"))
    return keyboard.as_markup()
