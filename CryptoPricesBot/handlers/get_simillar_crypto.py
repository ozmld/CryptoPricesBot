from fuzzywuzzy import process, fuzz

cryptos = []
with open("./database/crypto_names.txt", 'r') as f:
    for line in f.readlines():
        cryptos.append(line.rstrip())


def get_similar_cryptos(name, limit):
    return process.extract(name, cryptos, limit=limit)
# text = "etirium"
# print(get_similar_cryptos(text, 10, fuzz.ratio))
# print(get_similar_cryptos(text, 10, fuzz.QRatio))
# print(get_similar_cryptos(text, 10, fuzz.WRatio))
# print(get_similar_cryptos(text, 10, fuzz.UQRatio))
# print(get_similar_cryptos(text, 10, fuzz.partial_ratio))
# print(get_similar_cryptos(text, 10, fuzz.partial_token_set_ratio))
# print(get_similar_cryptos(text, 10, fuzz.partial_token_sort_ratio))
# print(get_similar_cryptos(text, 10, fuzz.token_set_ratio))
# print(get_similar_cryptos(text, 10, fuzz.token_sort_ratio))
# print(get_similar_cryptos(text, 10, fuzz.UWRatio))
