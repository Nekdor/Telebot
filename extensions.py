import telebot
import requests
import json
from config import currencies, HEADERS


def capital(string):
    """Функция делает первую букву строки большой, а остальные - маленькими."""
    return string[0].upper() + string[1:].lower()


class APIException(Exception):
    """Исключение обработки запроса пользователя"""
    pass


class Converter:
    """Класс-обработчик запроса пользователя"""
    @staticmethod
    def get_price(message: telebot.types.Message):
        """Статический метод, обрабатывающий запрос пользователя"""
        values = message.text.split(' ')  # Список введенных пользователем значений валют и суммы

        if len(values) != 3:  # Проверка количества введенных значений
            raise APIException('Введено неверное количество параметров')

        from_cur, to_cur, amount = list(map(capital, values))  # Переменные, хранящие значения валют и суммы

        try:  # Проверка наличия исходной валюты
            from_ticker = currencies[from_cur]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {from_cur}. Вероятно, ее нет в списке доступных валют')

        try:  # Проверка наличия целевой валюты
            to_ticker = currencies[to_cur]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {to_cur}. Вероятно, ее нет в списке доступных валют')

        try:  # Проверка того, что сумма является числом
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать количество {amount}. Вероятно, оно не является числом')

        if from_cur == to_cur:  # Проверка того, что целевая валюта не равна исходной
            raise APIException(f'Нельзя перевести валюту {from_cur} саму в себя')

        r = requests.request('GET',
                             url=f'https://api.apilayer.com/exchangerates_data/convert?to={to_ticker}'
                                 f'&from={from_ticker}&amount={amount}',
                             headers=HEADERS)  # Запрос до API
        answer = json.loads(r.content)['result']  # Результат
        text = f'{amount} ед. в валюте {from_cur} равно {answer} ед. в валюте {to_cur}'  # Текстовый ответ пользователю
        return text

