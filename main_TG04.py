import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, FSInputFile, InlineKeyboardMarkup, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage

from config import TOKEN
import keyboard1 as kb


bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.callback_query(F.data == 'news')
async def news(callback: CallbackQuery):
    await callback.answer("Новости подгружаются", show_alert=True)
    await callback.message.answer('Вот свежие новости', reply_markup=await kb.test_keyboard())


@dp.message(F.text == "Тестовая кнопа - 1")
async def test_button(message: Message):
   await message.answer('Обработка нажатия на reply кнопу - 1')

@dp.message(Command('help'))
async def help(message: Message):
    await message.answer("Этот бот умеет выполнять команды: \n/start \n/help")

# Обработчик команды /start
@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(f'Привет, {message.from_user.full_name}', reply_markup=kb.inline_keyboard_test)

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
