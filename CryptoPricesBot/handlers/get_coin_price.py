import cryptocompare


def get_coin_price(coin_tag):
    return cryptocompare.get_price(coin_tag, currency='RUB')[coin_tag]['RUB'],\
           cryptocompare.get_price(coin_tag, currency='USD')[coin_tag]['USD']

