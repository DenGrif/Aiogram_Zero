import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from config import TOKEN
from pyowm import OWM
import random

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Инициализация OpenWeatherMap с указанием языка
owm = OWM('c0e062f5ceaddc9438c305c317c0b9c2')
mgr = owm.weather_manager()

# Команда /help
@dp.message(Command('help'))
async def help_handler(message: Message):
    await message.answer("Этот бот умеет выполнять команды: \n/start \n/help")

# Команда /start
@dp.message(CommandStart())
async def start_handler(message: Message):
    await message.answer("Привет! Я бот 🤖, который подскажет погоду. Напиши название города, чтобы узнать погоду!")

# Обработка текстовых сообщений для получения погоды
@dp.message(F.text)
async def weather_handler(message: Message):
    try:
        # Получаем погоду для указанного города
        observation = mgr.weather_at_place(message.text)
        weather = observation.weather
        temp = weather.temperature('celsius')["temp"]
        wind = weather.wind()["speed"]
        status = weather.detailed_status  # Описание погоды

        # Перевод статуса на русский (если используется английский)
        translated_status = {
            "clear sky": "ясное небо",
            "few clouds": "малооблачно",
            "scattered clouds": "рассеянные облака",
            "broken clouds": "переменная облачность",
            "overcast clouds": "пасмурно",
            "light rain": "легкий дождь",
            "moderate rain": "умеренный дождь",
            "snow": "снег"
            # Добавьте другие переводы при необходимости
        }
        status_ru = translated_status.get(status, status)

        # Формируем ответ
        answer = (
            f"Температура сейчас в районе: {temp:.1f}°C\n"
            f"Скорость ветра: {wind} м/с\n"
            f"Погодные условия: {status_ru}\n"
        )

        if temp < 10:
            answer += "Очень холодно, одевайтесь теплее!"
        elif temp < 20:
            answer += "Прохладно, нужно что-то накинуть."
        elif temp > 32:
            answer += "Сильная жара, берегитесь солнца!"
        else:
            answer += "Температура комфортная!"

        await message.answer(answer)
    except Exception as e:
        await message.answer("Не удалось получить данные о погоде. Проверьте название города.")

# Запуск бота
async def main():
    try:
        await dp.start_polling(bot)
    except KeyboardInterrupt:
        print("\nБот остановлен.")

if __name__ == "__main__":
    asyncio.run(main())
