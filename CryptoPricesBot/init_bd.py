from pycoingecko import CoinGeckoAPI
from database import sqlite_db
cg = CoinGeckoAPI()
sqlite_db.sql_start()
for elem in cg.search(query="")['coins']:
    sqlite_db.sql_add_crypto(elem['name'], elem['symbol'], elem['large'], elem['id'])
names = sqlite_db.sql_get_all_names()
with open("./database/crypto_names.txt", 'w') as f:
    for name in names:
        f.write(name + "\n")