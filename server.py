import asyncio
import os
import logging

from aiogram import Bot, Dispatcher, executor, types
from request import get_lyrics, get_urls
from keyboards import prepare_keyboard


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
    \nExample: Boulevard Depo OFMD")


@dp.message_handler()
async def echo(message: types.Message):
    # old style:
    # await bot.send_message(message.chat.id, message.text)
    
    #try:
    d = {
        1 : 'a',
        2 : 'b', 
        3 : 'c'
    }
    keybkoard = prepare_keyboard(d)
    urls = get_urls(message.text)
    await message.answer(get_lyrics(urls[0]), reply_markup=keybkoard)
    await message.answer_photo(urls[1])
    print('OK:', message.text)

    # except:
    #     await message.answer("Sorry, I can't find that song(")
    #     print('FAIL:', message.text)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)