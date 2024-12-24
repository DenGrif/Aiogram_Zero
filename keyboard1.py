# переименован в Keyboard1 из Keyboard, так как это был lesson
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder


# Reply Клавиатура
main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Тестовая кнопа - 1")],
    [KeyboardButton(text="Тестовая кнопка - 2"), KeyboardButton(text="Тестовая кнопка - 3")]
], resize_keyboard=True)


# Inline клавиатура
inline_keyboard_test = InlineKeyboardMarkup(inline_keyboard=[
   [InlineKeyboardButton(text="Каталог", callback_data='catalog')],
   [InlineKeyboardButton(text="Новости", callback_data='news')],
   [InlineKeyboardButton(text="Профиль", callback_data='person')]
])

# билдер клавиатура второй вариант с Inline кнопками
test = ["кнопка 1", "кнопка 2", "кнопка 3", "кнопка 4"]

async def test_keyboard():
   keyboard = InlineKeyboardBuilder()
   for key in test:
       keyboard.add(InlineKeyboardButton(text=key, url='https://tv.yandex.ru/240?date=2024-07-13&period=all-day'))
   return keyboard.adjust(2).as_markup()


# билдер клавиатура первый вариант
# test = ["кнопка 1", "кнопка 2", "кнопка 3", "кнопка 4"]
#
# async def test_keyboard():
#     keyboard = ReplyKeyboardBuilder()
#     for key in test:
#         keyboard.add(KeyboardButton(text=key))
#     return keyboard.adjust(2).as_markup()