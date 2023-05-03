from aiogram import types, Dispatcher
from create_bot import bot
import hashlib
from database import sqlite_db
from handlers.get_simillar_crypto import get_similar_cryptos
from handlers.get_coin_price import get_coin_price
from handlers.text_repr import *
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.exceptions import MessageNotModified


def get_keyboard_update_price(coin_name, coin_tag, coin_id):
    keyboard_update_price = InlineKeyboardMarkup()
    keyboard_update_price.add(InlineKeyboardButton(text="Обновить цены",
                                                   callback_data=f'update prices; {coin_name}; {coin_tag}; {coin_id};'))
    return keyboard_update_price


async def inline_mode(query: types.InlineQuery):
    actions = []
    # creating inline item
    coins = get_similar_cryptos(query.query, 10)
    for name in coins:
        coin = sqlite_db.sql_get_coin_by_name(name[0])
        coin_tag = coin[1]
        coin_name = coin[0]
        coin_thumb = coin[2]
        coin_id = coin[3]
        coin_price_rub = coin[4]
        coin_price_usd = coin[5]
        # creating unique id
        result_id = hashlib.md5(coin_name.encode()).hexdigest()
        text = get_coin_price_text(coin_name, coin_tag, coin_price_rub, coin_price_usd, coin_id)
        input_content = types.InputTextMessageContent(text, parse_mode='html')
        title = coin[0] + f" ({coin_tag})"
        description = f"Нажмите, чтобы узнать текущую цену {title}"

        item = types.InlineQueryResultArticle(id=result_id,
                                              input_message_content=input_content,
                                              title=title,
                                              description=description,
                                              thumb_url=coin_thumb,
                                              reply_markup=get_keyboard_update_price(coin_name, coin_tag, coin_id)
                                              )
        actions.append(item)
    await bot.answer_inline_query(results=actions, cache_time=1, inline_query_id=query.id, is_personal=True)


async def start_command(message: types.Message):
    start_message = "Привет! Я бот, который позволит тебе узнать актуальный курс криптовалюты!" \
                    "\n\nЕсть вопросы как я работаю -> /help"
    await bot.send_message(message.chat.id, start_message, parse_mode="Markdown")


async def help_command(message: types.Message):
    bot_username = (await bot.get_chat_member(message.chat.id, bot.id)).user.username
    help_message = f"Чтобы узнать актуальный курс криптовалюты, напиши" \
                   f"\n@{bot_username} _название  криптотвалюты/её сокращение_" \
                   f"\n\nНапримеp:" \
                   f"\n@{bot_username} BTC" \
                   f"\n@{bot_username} Эфириум"
    await bot.send_message(message.chat.id, help_message, parse_mode="Markdown")


async def update_price(callback: types.CallbackQuery):
    coin_name = callback.data.split(";")[1][1:]
    coin_tag = callback.data.split(";")[2][1:]
    coin_id = callback.data.split(";")[3][1:]

    coin_price_rub, coin_price_usd = get_coin_price(coin_tag)

    sqlite_db.update_price(coin_name, coin_price_rub, coin_price_usd)

    text = get_coin_price_text(coin_name, coin_tag, coin_price_rub, coin_price_usd, coin_id)
    try:
        await bot.edit_message_text(inline_message_id=callback.inline_message_id,
                                    text=text,
                                    parse_mode='html',
                                    reply_markup=get_keyboard_update_price(coin_name, coin_tag, coin_id),
                                    )
    except MessageNotModified:
        pass

    await callback.answer()


def register_handlers_general(dp: Dispatcher):
    dp.register_message_handler(start_command, commands=['start'])
    dp.register_message_handler(help_command, commands=['help'])

    dp.register_callback_query_handler(update_price)
    dp.register_inline_handler(inline_mode)
