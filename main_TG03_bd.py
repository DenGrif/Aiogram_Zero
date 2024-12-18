import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, FSInputFile
from config import TOKEN
import sqlite3

bot = Bot(token=TOKEN)
dp = Dispatcher()



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
