import asyncio
from datetime import datetime, timedelta
import random

import requests
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, CallbackQuery
from config import TOKEN, NASA_API_KEY
import keyboard as kb

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Функция для получения случайной APOD
def get_random_apod():
   end_date = datetime.now()
   start_date = end_date - timedelta(days=365)
   random_date = start_date + (end_date - start_date) * random.random()
   date_str = random_date.strftime("%Y-%m-%d")

   url = f'https://api.nasa.gov/planetary/apod?api_key={NASA_API_KEY}&date={date_str}'
   response = requests.get(url)
   return response.json()

# Команда /random_apod
@dp.message(Command("random_apod"))
async def random_apod(message: Message):
   apod = get_random_apod()
   photo_url = apod['url']
   title = apod['title']

   await message.answer_photo(photo=photo_url, caption=f"{title}")

# Команда /start
@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(
        f"Привет, {message.from_user.full_name}! 🤖\n\n"
        f"Этот бот умеет показывать случайные фото и видео космического изображения дня из (Astronomic Picture Of the Day = apod)APOD NASA.\n\n"
        f"Доступные команды:\n"
        f"/start - Приветствие и список команд\n"
        f"/random_apod - Случайное фото или видео дня от NASA 🌌"
    )

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
