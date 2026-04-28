from enum import StrEnum


class Environment(StrEnum):
    """Перечень поддерживаемых окружений для запуска тестов"""
    DEV = 'dev'
    PROD = 'prod'

    def __str__(self):
        """Название окружения с заглавной буквы для логов/отчётов"""
        return self.value.capitalize()




_URLS: dict[Environment, str] = {
    Environment.DEV: "https://restful-booker.herokuapp.com",
    Environment.PROD: "https://restful-booker.herokuapp.com",
}




# print(_URLS[Environment.DEV])