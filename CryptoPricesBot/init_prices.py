from pycoingecko import CoinGeckoAPI
from database import sqlite_db
cg = CoinGeckoAPI()
sqlite_db.sql_start()

for page in range(26, 60):
    coins_rub = cg.get_coins_markets(vs_currency=['RUB'], per_page=250, page=page)
    coins_usd = cg.get_coins_markets(vs_currency=['USD'], per_page=250, page=page)
    for i in range(len(coins_usd)):
        coin = coins_usd[i]
        sqlite_db.update_price(coin['name'], price_usd=coin['current_price'])
    for i in range(len(coins_rub)):
        coin = coins_rub[i]
        sqlite_db.update_price(coin['name'], price_rub=coin['current_price'])
    if len(coins_rub) == 0 and len(coins_usd) == 0:
        break
    print(page)