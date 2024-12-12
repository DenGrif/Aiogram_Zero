import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from config import TOKEN
import random

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command('photo'))
async def photo(message: Message):
    responses = ['https://i.pinimg.com/736x/5e/13/08/5e130873b4f7885e3d45e9755c2414b7.jpg',
                 'https://soundex.ru/forum/uploads/monthly_2022_03/1577338889_004.jpg.ff063a5b17dc60ab168473e27737355a.jpg',
                 'https://i.pinimg.com/474x/c0/88/c1/c088c1ef5789634bedabda776766f8bf.jpg']
    rand_photo = random.choice(responses)
    await message.answer_photo(photo=rand_photo, caption='Ух ты, классная фотка')

@dp.message(F.photo)
async def react_photo(message: Message):
    responses = ['Ого, какая фотка!', 'Непонятно, что это такое', 'Не отправляй мне такое больше']
    rand_answ = random.choice(responses)
    await message.answer(rand_answ)

@dp.message(F.text == "что такое ИИ?")
async def aitext(message: Message):
    await message.answer('Искусственный интеллект — это свойство искусственных интеллектуальных систем выполнять творческие функции')

@dp.message(Command('help'))
async def help(message: Message):
    await message.answer("Этот бот умеет выполнять команды: \n/start \n/help \n/photo")

@dp.message(CommandStart())
async def start(message: Message):
    await message.answer("Приветики, я бот! Бот 🤖 находится в стадии разработки!")

async def main():
    await dp.start_polling(bot)

async def main():
    try:
        await dp.start_polling(bot)
    except KeyboardInterrupt:
        print("\nБот остановлен.")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nПрограмма завершена.")

# Что изменено?
#     1. Добавлено исключение KeyboardInterrupt в блоке try для обработки в функции
# main и главном блоке if __name__ == "__main__".
#     2. Теперь при завершении программы вы увидите сообщение "Бот остановлен."
# или "Программа завершена." вместо стека ошибок.
# Это улучшит читаемость вывода при завершении программы и избавит от лишнего шума в терминале.






