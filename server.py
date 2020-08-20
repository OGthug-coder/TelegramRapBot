"""
    Main file of my telegram bot
"""
import os
import logging
import exceptions

from aiogram import Bot, Dispatcher, executor, types
from request import get_lyrics, get_urls
from keyboards import prepare_keyboard


API_TOKEN = '1337211989:AAEjy17drLm_uuG-Zfcq-aRwOZ8nDRjCLK4'
# os.environ["TELEGRAM_BOT_TOKEN"]

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    filename='app.log',
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%d-%b-%y %H:%M:%S'
)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

def split_on_two(stroke):
    """
    Function that splits very long text on two strings
    """
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
    """
        Processing of keyboard callback
    """

    key = int(callback_query.data)

    try:
        url = DATA[key]['url']
        
    except exceptions.AsyncError:
        pass

    image_url = DATA[key]['image_url']

    try:
        text = get_lyrics(url)
        if len(text) > 4000:
            first, second = split_on_two(text)
            await bot.send_message(callback_query.from_user.id, first)
            await bot.send_message(callback_query.from_user.id, second)

        else:
            await bot.send_message(callback_query.from_user.id, get_lyrics(url))

        await bot.send_photo(callback_query.from_user.id, image_url)
        logging.info('OK: %s', url)

    except exceptions.ParseError:
        await bot.send_message(callback_query.from_user.id, "Sorry, I can't scrap that song(")
        logging.warning('FAIL: %s', url)

@dp.message_handler()
async def message_processing(message: types.Message):
    """
        Function that processing user's messages
    """
    global DATA
    DATA, keyboard_data = get_urls(message.text)
    keyboard = prepare_keyboard(keyboard_data)

    if keyboard["inline_keyboard"] != []:
        await message.answer(message.text, reply_markup=keyboard)
    else:
        await message.answer("Sorry, I can't find that song(")
        logging.info('No results found: %s', message.text)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
