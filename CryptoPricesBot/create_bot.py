from aiogram import Bot
from aiogram.dispatcher import Dispatcher

# getting TOKEN and creating the bot and dispatcher
with open("put_token_here", 'r') as f:
    TOKEN = f.readline().rstrip()

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
