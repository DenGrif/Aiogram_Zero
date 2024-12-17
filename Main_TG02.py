import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, FSInputFile
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from config import TOKEN
import random
from translate import Translator

bot = Bot(token=TOKEN)
dp = Dispatcher(storage=MemoryStorage())

# Инициализация переводчика
translator = Translator(to_lang="en")

# Состояния для работы переводчика
class TranslationState(StatesGroup):
    waiting_for_text = State()

# Обработчик команды /start
@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(f'Привет, {message.from_user.full_name}!\n'
                         f'Для перевода текста используйте команду /tr.\n'
                         f'Чтобы отправить голосовое сообщение, используйте команду /voice.')

# Обработчик фото
@dp.message(F.photo)
async def react_photo(message: Message):
    responses = ['Ого, какая фотка!', 'Непонятно, что это такое', 'Не отправляй мне такое больше']
    rand_answ = random.choice(responses)
    await message.answer(rand_answ)
    # Сохраняем фото на сервере
    await message.photo[-1].download(destination=f'img/{message.photo[-1].file_id}.jpg')

# Обработчик команды /translate
@dp.message(Command("tr"))
async def start_translation(message: Message, state: FSMContext):
    await message.answer("Введите текст, который нужно перевести на английский.")
    await state.set_state(TranslationState.waiting_for_text)

# Обработка текста для перевода (в состоянии)
@dp.message(TranslationState.waiting_for_text)
async def translate_text(message: Message, state: FSMContext):
    try:
        # Явно указываем язык источника (русский -> английский)
        translator = Translator(from_lang="ru", to_lang="en")
        translated_text = translator.translate(message.text)
        await message.answer(f"Перевод на английский:\n{translated_text}")
    except Exception as e:
        await message.answer("Произошла ошибка при переводе текста.")
    finally:
        await state.clear()

# Обработчик команды /voice: отправка голосового сообщения
@dp.message(Command("voice"))
async def send_voice(message: Message):
    try:
        voice_path = "audio/sample_voice.ogg"  # Путь к файлу голосового сообщения
        voice_file = FSInputFile(voice_path)
        await message.answer_voice(voice_file)
    except Exception as e:
        await message.answer("Не удалось отправить голосовое сообщение. Проверьте файл.")

# Основной цикл
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
