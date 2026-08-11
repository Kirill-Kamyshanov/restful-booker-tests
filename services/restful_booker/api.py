from config.environments import EnvironmentConfig
from services.restful_booker.auth.client import AuthClient
from services.restful_booker.booking.client import BookingClient
from services.restful_booker.ping.client import PingClient


class RestfulBookerApi:
    """Точка входа для тестов: один объект с фасадами по всем ресурсам сервиса restful-booker."""

    def __init__(self, env_config: EnvironmentConfig):
        """Инициализирует клиенты всех ресурсов на одном env_config (общая конфигурация и authorization)."""
        self.booking = BookingClient(env_config)
        self.auth = AuthClient(env_config)
        self.ping = PingClient(env_config)
