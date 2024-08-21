import asyncio
import random
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, FSInputFile
from config import TOKEN
from gtts import gTTS
import os

bot = Bot(token=TOKEN)
dp = Dispatcher()


# Команда /start
@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(f"Приветствую, {message.from_user.full_name}. Я Бот!")


# Команда /help
@dp.message(Command("help"))
async def help(message: Message):
    await message.answer(
        "Этот бот умеет выполнять команды: \n /start - запуск бота \n /photo - случайное фото \n /help - помощь")


# Команда /photo
@dp.message(Command("photo"))
async def photo(message: Message):
    photos = [
        "https://sofmix-shop.ru/upload/iblock/ef2/rk3qb096rwe8256x0b9i2iubqlh2rly1.jpg",
        "https://baldezh.top/uploads/posts/2022-08/1660006712_32-funart-pro-p-iskusstvennii-intellekt-art-krasivo-35.jpg",
        "https://trashbox.ru/ifiles/1407921_55b940_logo/prodvinutyj-ii-openai-obmanuli-pri-pomoschi-ruchki-i-bumagi-1.jpeg"
    ]
    rand_photo = random.choice(photos)
    await message.answer_photo(photo=rand_photo, caption="Это случайное фото с ИИ!")


@dp.message(Command("video"))
async def video(message: Message):
    await bot.send_chat_action(message.chat.id, "upload_video")
    video = FSInputFile("video.mp4")
    await bot.send_video(message.chat.id, video)


@dp.message(Command("voice"))
async def voice(message: Message):
    voice = FSInputFile("voice.ogg")
    await bot.send_voice(message.chat.id, voice)

@dp.message(Command("audio"))
async def audio(message: Message):
    audio = FSInputFile("audio.mp3")
    await bot.send_audio(message.chat.id, audio)


@dp.message(Command('training'))
async def training(message: Message):
    training_list = [
        "Тренировка 1: \n 1. Скручивания: 3 подхода по 15 повторений \n 2. Велосипед: 3 подхода по 20 повторений (каждая сторона) \n 3. Планка: 3 подхода по 30 секунд",
        "Тренировка 2: \n 1. Подъемы ног: 3 подхода по 15 повторений \n 2. Русский твист: 3 подхода по 20 повторений (каждая сторона) \n 3. Планка с поднятой ногой: 3 подхода по 20 секунд (каждая нога)",
        "Тренировка 3: \n 1. Скручивания с поднятыми ногами: 3 подхода по 15 повторений \n 2. Горизонтальные ножницы: 3 подхода по 20 повторений \n 3. Боковая планка: 3 подхода по 20 секунд (каждая сторона)"
    ]
    rand_tr = random.choice(training_list)
    await message.answer(f"Это ваша мини-тренировка на сегодня {rand_tr}")

    tts = gTTS(rand_tr, lang="ru")
    tts.save("training.ogg")
    audio = FSInputFile("training.ogg3")
    await bot.send_voice(message.chat.id, audio)

    os.remove("training.ogg")


# Обработка текста "Что такое ИИ?"
@dp.message(F.text == "Что такое ИИ?")
async def aitext(message: Message):
    await message.answer(
        "Искусственный интеллект – раздел информатики, который занимается решением когнитивных задач, обычно отведенных человеку. К таким задачам относятся обучение, создание и распознавание образов.")


# Реакция на фото
@dp.message(F.photo)
async def react_photo(message: Message):
    await message.answer("Ого, какое фото!")
    await bot.download(message.photo[-1], destination=f'tmp/{message.photo[-1].file_id}.jpg')


@dp.message()
async def echo(message: Message):
    await message.send_copy(chat_id=message.chat.id)


# Запуск бота
async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
