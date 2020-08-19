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

def split_on_two(stroke):
    first = stroke[:4000]
    second = stroke[4000:]
    return first, second

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    await message.answer("Hi!\nI'm RapBot!\nWhich song lyrics do you want to see?\
    \nExample: Boulevard Depo OFMD")


@dp.callback_query_handler(lambda c: True)
async def process_callback(callback_query: types.CallbackQuery):
    
    key = int(callback_query.data)
    url = data[key]['url']
    image_url = data[key]['image_url']

    try:
        text = get_lyrics(url)
        if len(text) > 4000:
            first, second = split_on_two(text)
            await bot.send_message(callback_query.from_user.id, first)
            await bot.send_message(callback_query.from_user.id, second)

        else:
            await bot.send_message(callback_query.from_user.id, get_lyrics(url))

        await bot.send_photo(callback_query.from_user.id, image_url)
        print('OK:', url)

    except:
        await bot.send_message(callback_query.from_user.id, "Sorry, I can't scrap that song(")
        print('FAIL:', url)

@dp.message_handler()
async def echo(message: types.Message):

    global data, query
    data, keyboard_data = get_urls(message.text)
    keyboard = prepare_keyboard(keyboard_data)
    query = message.text

    if keyboard["inline_keyboard"] != []:
        await message.answer(message.text, reply_markup=keyboard)
    else:
        await message.answer("Sorry, I can't find that song(")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)