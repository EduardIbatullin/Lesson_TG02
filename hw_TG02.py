import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, FSInputFile
from config import TOKEN
from gtts import gTTS
import os
from deep_translator import GoogleTranslator

bot = Bot(token=TOKEN)
dp = Dispatcher()


# Команда /start
@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(f"Приветствую, {message.from_user.full_name}. Я Бот!")


# Команда /help
@dp.message(Command("help"))
async def help_command(message: Message):
    await message.answer(
        "Доступные команды:\n"
        "/start - Запуск бота\n"
        "/help - Получить список доступных команд\n"
        "Отправка фото - Бот сохранит ваше фото в папку img\n"
        "Отправь голосовое сообщение - Бот отправит голосовое сообщение\n"
        "Любой текст - Бот переведет текст на английский язык и отправит его в виде голосового сообщения"
    )


# Реакция на фото и сохранение его в папку img
@dp.message(F.photo)
async def save_photo(message: Message):
    file_id = message.photo[-1].file_id
    file_path = f'img/{file_id}.jpg'
    await bot.download(file_id, destination=file_path)
    await message.answer("Фото сохранено!")


# Отправка голосового сообщения
@dp.message(F.text == "Отправь голосовое сообщение")
async def send_voice_message(message: Message):
    text = "Это голосовое сообщение"
    tts = gTTS(text, lang="ru")
    tts.save("voice.ogg")
    voice = FSInputFile("voice.ogg")
    await bot.send_voice(message.chat.id, voice)
    os.remove("voice.ogg")


# Перевод текста на английский язык и отправка его как текстом, так и голосом
@dp.message(F.text)
async def translate_and_send_voice(message: Message):
    # Перевод текста
    translated_text = GoogleTranslator(source='auto', target='en').translate(message.text)

    # Отправка переведенного текста
    await message.answer(translated_text)

    # Создание и отправка голосового сообщения с переводом
    tts = gTTS(translated_text, lang="en")
    tts.save("translated_voice.ogg")
    voice = FSInputFile("translated_voice.ogg")
    await bot.send_voice(message.chat.id, voice)
    os.remove("translated_voice.ogg")


# Запуск бота
async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
