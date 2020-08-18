import asyncio
import os
import logging

from aiogram import Bot, Dispatcher, executor, types
from request import get_lyrics, get_url


API_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    await message.answer("Hi!\nI'm RapBot!\nWhich song lyrics do you want to see?\
    \nExample: Boulevard Depo - OFMD")


@dp.message_handler()
async def echo(message: types.Message):
    # old style:
    # await bot.send_message(message.chat.id, message.text)
    
    try:
        await message.answer(get_lyrics(get_url(message.text)))
        print('OK:', message.text)
    except:
        await message.answer("Sorry, I can't find that song(")
        print('FAIL:', message.text)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)