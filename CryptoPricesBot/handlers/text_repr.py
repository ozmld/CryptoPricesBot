BASE_URL = "https://www.coingecko.com/en/coins/"


def get_coin_price_text(coin_name, coin_tag, coin_price_rub, coin_price_usd, coin_id):
    base_text = f"Цена монеты <a href=\"{BASE_URL + coin_id}\">{coin_name} ({coin_tag})</a> "
    if coin_price_rub == "" and coin_price_usd == "":
        base_text += f"мне неизвестна :("
    elif coin_price_usd == "":
        base_text += f"составляет {coin_price_rub}₽"
    elif coin_price_rub == "":
        base_text += f"составляет {coin_price_usd}$"
    else:
        base_text += f"составляет {coin_price_rub}₽ или {coin_price_usd}$"

    return base_text
