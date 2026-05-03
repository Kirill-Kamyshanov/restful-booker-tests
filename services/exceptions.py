class ApiError(Exception):
    """Базовая ошибка API-клиента (сеть, таймаут, неизвестный сбой транспорта)."""


class ApiTimeoutError(ApiError):
    """Превышен таймаут ответа сервиса."""


class ApiConnectionError(ApiError):
    """Не удалось установить соединение с сервисом."""
