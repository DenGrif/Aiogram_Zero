import asyncio
from datetime import datetime, timedelta
import random
import requests
from aiogram import Bot, Dispatcher
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from config import TOKEN, WEATHER_API_KEY, THE_CAT_API_KEY, NASA_API_KEY
from keyboard2 import main as main_keyboard

# Инициализация бота
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Функции API
def get_weather(city_name: str):
    from pyowm import OWM
    owm = OWM(WEATHER_API_KEY)
    mgr = owm.weather_manager()
    try:
        observation = mgr.weather_at_place(city_name)
        weather = observation.weather
        temp = weather.temperature('celsius')["temp"]
        wind = weather.wind()["speed"]
        status = weather.detailed_status

        # Перевод статуса на русский
        translated_status = {
            "clear sky": "ясное небо",
            "few clouds": "малооблачно",
            "scattered clouds": "рассеянные облака",
            "broken clouds": "переменная облачность",
            "overcast clouds": "пасмурно",
            "light rain": "легкий дождь",
            "moderate rain": "умеренный дождь",
            "snow": "снег"
        }
        status_ru = translated_status.get(status, status)
        return f"Температура: {temp:.1f}°C\nСкорость ветра: {wind} м/с\nПогодные условия: {status_ru}"
    except Exception:
        return "Не удалось получить данные о погоде. Проверьте название города."

def get_random_apod():
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365)
    random_date = start_date + (end_date - start_date) * random.random()
    date_str = random_date.strftime("%Y-%m-%d")

    url = f'https://api.nasa.gov/planetary/apod?api_key={NASA_API_KEY}&date={date_str}'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return {"url": "", "title": "Не удалось получить фото NASA"}

def get_breed_info(breed_name):
    url = "https://api.thecatapi.com/v1/breeds"
    headers = {"x-api-key": THE_CAT_API_KEY}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        breeds = response.json()
        for breed in breeds:
            if breed['name'].lower() == breed_name.lower():
                return breed
    return None

def get_cat_image_by_breed(breed_id):
    url = f"https://api.thecatapi.com/v1/images/search?breed_ids={breed_id}"
    headers = {"x-api-key": THE_CAT_API_KEY}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        return data[0]['url'] if data else None
    return None

# Обработчики команд
@dp.message(CommandStart())
async def start_handler(message: Message):
    await message.answer(
        f"Привет, {message.from_user.full_name}! 🤖\n\n"
        f"Этот бот умеет:\n"
        f"🌤 Показывать погоду по названию города\n"
        f"🌌 Отправлять случайное фото или видео из NASA APOD\n"
        f"🐾 Предоставлять информацию о породах кошек\n\n"
        f"Выберите действие с помощью кнопок ниже или используйте команды:\n"
        f"/weather - Узнать погоду\n"
        f"/random_apod - Фото NASA\n"
        f"/cats - Информация о породах кошек",
        reply_markup=main_keyboard
    )

@dp.message(Command("random_apod"))
async def random_apod_handler(message: Message):
    apod = get_random_apod()
    if apod['url']:
        await message.answer_photo(photo=apod['url'], caption=apod['title'])
    else:
        await message.answer("Не удалось получить фото NASA.")

@dp.message(Command("weather"))
async def weather_start_handler(message: Message):
    await message.answer("Напишите название города, чтобы узнать погоду.")

@dp.message(Command("cats"))
async def cats_start_handler(message: Message):
    await message.answer("Напишите название породы кошки, чтобы получить информацию о ней.")

@dp.message()
async def general_message_handler(message: Message):
    if message.text.lower() == "погода":
        await message.answer("Напишите название города, чтобы узнать погоду.")
    elif message.text.lower() == "фото наса":
        apod = get_random_apod()
        if apod['url']:
            await message.answer_photo(photo=apod['url'], caption=apod['title'])
        else:
            await message.answer("Не удалось получить фото NASA.")
    elif message.text.lower() == "породы кошек":
        await message.answer("Напишите название породы кошки, чтобы получить информацию о ней.")
    else:
        if message.text:  # Проверяем, что пользователь ввел текст
            city_name = message.text.strip()
            weather_info = get_weather(city_name)
            if weather_info.startswith("Температура"):
                await message.answer(weather_info)
            else:
                breed_info = get_breed_info(city_name)
                if breed_info:
                    image_url = get_cat_image_by_breed(breed_info['id'])
                    info = (
                        f"Порода: {breed_info['name']}\n"
                        f"Описание: {breed_info['description']}\n"
                        f"Продолжительность жизни: {breed_info['life_span']} лет"
                    )
                    if image_url:
                        await message.answer_photo(photo=image_url, caption=info)
                    else:
                        await message.answer(info)
                else:
                    await message.answer("Не удалось распознать запрос. Проверьте данные.")
        else:
            await message.answer("Я не понимаю ваш запрос. Используйте команды или кнопки.")


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
