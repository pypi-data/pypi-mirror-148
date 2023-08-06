"""Ошибки"""


class ServerError(Exception):
    """Класс - исключение, для обработки ошибок сервера"""
    def __init__(self, text):
        self.text = text

    def __str__(self):
        return self.text


class ReqFieldMissingError(Exception):
    """Класс - исключение отсутствует обязательное поле в принятом словаре"""
    def __init__(self, missing_field):
        self.missing_field = missing_field

    def __str__(self):
        return f'В принятом словаре отсутствует обязательное поле {self.missing_field}.'


class IncorrectDataRecivedError(Exception):
    """Класс - исключение некорректные данные получены от сокета"""
    def __str__(self):
        return 'Принято некорректное сообщение от удалённого компьютера.'
