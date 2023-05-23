import telebot
from Config1 import keys, TOKEN
from Extension1 import APIException, Converter

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start(message: telebot.types.Message):
    text = 'Привет! Я Чат бот обмена валют.\n ' 'Для начала работы введите данные в следующем формате (через пробел):' \
           ' \n<Название валюты для конвертации>  \n<Название валюты в которую надо перевести> ' \
           '\n<Сумму в числовом формате>\n \
 Список доступных валют: /values'
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key,))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text', ])
def get_price(message: telebot.types.Message):
    try:
        values = message.text.split(' ')
        if len(values) != 3:
            raise APIException('Неверное колличество параметров, введите 3 параметра')

        base, quote, amount = values
        total_base = Converter.get_price(base, quote, amount)
        total_base *= float(amount)
        total_base = round(total_base, 2)
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя: \n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось выполнить команду\n{e}')
    else:
        text = f'Цена {quote} в {base} \n {amount} {quote} = {total_base} {base}'
        bot.send_message(message.chat.id, text)

bot.polling(none_stop=True)
