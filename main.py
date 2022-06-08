import telebot
from config import TOKEN, currencies
from extensions import APIException, Converter

bot = telebot.TeleBot(TOKEN)  # Создание объекта-бота


@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    """Обработчик команды вызова справки"""
    text = 'Для перевода валюты введите команду в следующем виде:\n<название исходной валюты> ' \
           '<название валюты, в которую надо перевести> <сумма в исходной валюте>\n' \
           'Для просмотра доступных валют введите команду /currencies'
    bot.reply_to(message, text)


@bot.message_handler(commands=['currencies'])
def availible_currencies(message: telebot.types.Message):
    """Обработчик команды просмотра доступных валют"""
    text = 'Доступные валюты: '
    for k in currencies.keys():
        text += f'\n{k}'
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    """Обработчик запроса на перевод валюты"""
    try:  # Попытка получить ответ с помощью метода-обработчика
        answer = Converter.get_price(message)
    except APIException as e:  # В случае неверного запроса выводится информация об ошибке пользователя
        bot.reply_to(message, f'Возникла ошибка пользователя:\n{e}')
    except Exception as e:  # В случае ошибки на сервере информация о ней выводится пользователю
        bot.reply_to(message, f'Не удалось обработать запрос, поскольку возникла следующая ошибка\n{e}')
    else:  # Если ошибок не возникло, пользователю выводится ответ
        bot.reply_to(message, answer)


bot.polling()  # Запуск бота
