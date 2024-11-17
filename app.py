import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
import os
from dotenv import load_dotenv
from src.AkashaQA import AkashaQA
import re

load_dotenv()
API_KEY_BOT = os.getenv("API_KEY_TG")

akasha = AkashaQA()

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_KEY_BOT)
dp = Dispatcher(bot=bot)


@dp.message(CommandStart())
async def start(message: types.Message):
    await message.answer(
        "🌌 *Hello, Traveler!* 🌌\n\n"
        "_I'm Akasha, the Genshin Impact knowledge keeper._ 💫\n"
        "What _forbidden knowledge_ do you seek today? 📜",
        parse_mode="Markdown"
    )


@dp.message()
async def answer_question(message: types.Message):
    waiting_message = await message.reply(
        "_🌠 Seeking the secrets of Teyvat... Please hold... 🌌_",
        parse_mode="Markdown"
    )

    question = message.text
    answer = akasha.get_answer(question)

    print(answer)

    await bot.edit_message_text(
        answer,
        chat_id=message.chat.id,
        message_id=waiting_message.message_id,
        parse_mode="Markdown"
    )


async def run_bot():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(run_bot())
