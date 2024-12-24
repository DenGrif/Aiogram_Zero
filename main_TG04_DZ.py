import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, CallbackQuery
from config import TOKEN
import keyboard as kb

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Обработчик команды /start
@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(
        f"Привет, {message.from_user.full_name}! Команды в этом боте: \n/start \n/links \n/dynamic",
        reply_markup=kb.main_menu
    )

# Ответ на кнопки "Привет" и "Пока"
@dp.message(F.text == "Привет")
async def say_hello(message: Message):
    await message.answer(f"Привет, {message.from_user.full_name}!")

@dp.message(F.text == "Пока")
async def say_goodbye(message: Message):
    await message.answer(f"До свидания, {message.from_user.full_name}!")

# Обработчик команды /links
@dp.message(Command("links"))
async def links(message: Message):
    await message.answer("Вот ссылки, которые могут быть полезны:", reply_markup=kb.links_keyboard)

# Обработчик команды /dynamic
@dp.message(Command("dynamic"))
async def dynamic_menu(message: Message):
    await message.answer("Нажмите кнопку ниже:", reply_markup=kb.dynamic_keyboard())

# Обработчик нажатий на динамические кнопки
@dp.callback_query(F.data == "show_more")
async def show_more(callback: CallbackQuery):
    await callback.message.edit_reply_markup(reply_markup=kb.expanded_keyboard())

@dp.callback_query(F.data.in_({"option_1", "option_2"}))
async def option_selected(callback: CallbackQuery):
    option = "Опция 1" if callback.data == "option_1" else "Опция 2"
    await callback.message.answer(f"Вы выбрали: {option}")

# Запуск бота
async def main():
    try:
        print("Бот запущен...")
        await dp.start_polling(bot)
    except KeyboardInterrupt:
        print("\nБот остановлен.")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nПрограмма завершена.")
