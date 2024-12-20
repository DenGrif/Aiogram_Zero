import asyncio
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage

from config import TOKEN
import sqlite3
import logging

# Конфигурация бота
bot = Bot(token=TOKEN)
dp = Dispatcher()
storage = MemoryStorage()

logging.basicConfig(level=logging.INFO)

# Состояния
class Form(StatesGroup):
    name = State()
    age = State()
    grade = State()

# Инициализация базы данных
def init_db():
    conn = sqlite3.connect("school_data.db")
    cur = conn.cursor()
    cur.execute('''
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        age INTEGER NOT NULL,
        grade TEXT NOT NULL
    )''')
    conn.commit()
    conn.close()

init_db()

# Хендлер для команды /start
@dp.message(CommandStart())
async def start(message: Message, state: FSMContext):
    await message.answer("Привет! Как тебя зовут?")
    await state.set_state(Form.name)

# Хендлер для имени
@dp.message(Form.name)
async def get_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Сколько тебе лет?")
    await state.set_state(Form.age)

# Хендлер для возраста
@dp.message(Form.age)
async def get_age(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("Пожалуйста, введи число.")
        return
    await state.update_data(age=int(message.text))
    await message.answer("В каком ты классе?")
    await state.set_state(Form.grade)

# Хендлер для класса
@dp.message(Form.grade)
async def get_grade(message: Message, state: FSMContext):
    user_data = await state.get_data()
    user_data["grade"] = message.text

    # Сохранение данных в базу данных
    conn = sqlite3.connect("school_data.db")
    cur = conn.cursor()
    cur.execute('''
    INSERT INTO students (name, age, grade) VALUES (?, ?, ?)''',
                (user_data["name"], user_data["age"], user_data["grade"]))
    conn.commit()
    conn.close()

    await message.answer(f"Спасибо! Твои данные сохранены:\n"
                         f"Имя: {user_data['name']}\n"
                         f"Возраст: {user_data['age']}\n"
                         f"Класс: {user_data['grade']}")
    await state.clear()

# Основной цикл
async def main():
    try:
        print("Бот запущен...")
        await dp.start_polling(bot)
    except KeyboardInterrupt:
        print("Бот остановлен.")
    finally:
        await bot.session.close()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Программа завершена.")

