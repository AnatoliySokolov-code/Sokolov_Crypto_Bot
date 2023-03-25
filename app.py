import json

import telebot

import json

import requests

TOKEN = '6187649235:AAE5nEsCEcJnkb4-7_P44YoYzt3VfEbViCY'


bot = telebot.TeleBot(TOKEN)
keys = {
    'биткоин': 'BTC',
    'эфириум': 'ETH',
    'доллар': 'USD',
    'евро': 'EUR',
    'рубль': 'RUB',
    'тенге': 'KZT',
    'юань': 'CNY',
}


class ConvertionException(Exception):
    pass

class CryptoConverter:
    @staticmethod
    def convert(self, quote: str, base: str, amount: str):
        if quote == base:
            raise ConvertionException(f'Невозможно перевести одинаковые валюты {base}.'

    try:
            quote_ticker = keys[quote]
        except KeyError:
            raise ConvertionException(f'Не удалось обработать валюту {quote}')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise ConvertionException(f'Не удалось обработать валюту {base}')

        try:
            amount = float(amount)
        except ValueError:
            raise ConvertionException(f'Не удалось обработать количество {amount}')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
        total_base = json.loads(r.content)[keys[base]]
        return total_base


@bot.message_handler(commands=['start', 'help'])
def echo_test(message: telebot.types.Message):
    text = ' Чтобы начать работу введите боту команду в следующем формате: \n<имя валюты> \
< в какую валюту перевести> \
<количество переводимой валюты>\n увидеть список всех доступных валют: /values'
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text',])
def convert(message: telebot.types.Message):
    values = message.text.split(' ')

    if len(values) != 3:
        raise ConvertionException('Вы ввели слишком мало или много параметров.')

    quote, base, amount = values
    total_base = CryptoConverter.convert(quote, base, amount )

    text = f'Цена {amount} {quote} в {base} - {total_base}'
    bot.send_message(message.chat.id, text)


bot.polling()