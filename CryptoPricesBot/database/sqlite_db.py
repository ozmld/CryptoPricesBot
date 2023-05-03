import sqlite3 as sq


def sql_start():
    global base, cur
    base = sq.connect("CryptoCur.db")
    cur = base.cursor()
    if base:
        print("Base connected!")
    base.execute('CREATE TABLE IF NOT EXISTS crypto(name TEXT PRIMARY KEY, symbol TEXT, thumb TEXT, id TEXT, price_rub TEXT, price_usd TEXT)')
    base.commit()

def sql_add_crypto(name, symbol, thumb, id):
    crypto = cur.execute("SELECT * FROM crypto WHERE name == \"{}\" LIMIT 1".format(name)).fetchall()
    if not crypto:
        cur.execute('INSERT INTO crypto VALUES (?, ?, ?, ?, ?, ?)', (name, symbol, thumb, id, "", ""))
        base.commit()

def update_price(name, price_rub="", price_usd=""):
    if price_usd == "" == price_rub:
        return
    if (price_usd == ""):
        cur.execute("UPDATE crypto SET price_rub = \"{}\" WHERE name == \"{}\";".format(price_rub, name)).fetchall()
    elif price_rub == "":
        cur.execute("UPDATE crypto SET price_usd = \"{}\" WHERE name == \"{}\";".format(price_usd, name)).fetchall()
    else:
        cur.execute("UPDATE crypto SET price_rub = \"{}\", price_usd = \"{}\" WHERE name == \"{}\";".format(price_rub, price_usd, name)).fetchall()
    base.commit()

def sql_get_coin_by_name(name):
    return cur.execute("SELECT * FROM crypto WHERE name == \"{}\" LIMIT 1".format(name)).fetchall()[0]


def sql_get_all_names():
    crypto = cur.execute("SELECT * FROM crypto").fetchall()
    crypto = [name[0] for name in crypto]
    return crypto


def sql_get_all_tags():
    crypto = cur.execute("SELECT * FROM crypto").fetchall()
    crypto = [name[1] for name in crypto]
    return crypto



