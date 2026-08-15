from enum import StrEnum

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Environment(StrEnum):
    """Перечень поддерживаемых окружений для запуска тестов"""

    DEV = "dev"
    STAGE = "stage"

    def __str__(self):
        """Название окружения с заглавной буквы для логов/отчётов"""
        return self.value.capitalize()


_URLS: dict[Environment, str] = {
    Environment.DEV: "https://restful-booker.herokuapp.com",
    Environment.STAGE: "https://restful-booker.herokuapp.com",
}


class EnvironmentConfig(BaseSettings):
    """Конфиг окружения. URL фиксированы в коде, секреты подтягиваются из .env / переменных окружения."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_prefix="",
        extra="ignore",
        case_sensitive=False,
    )

    booking_url: str
    booker_username: str
    booker_password: str
    authorization: str = Field(default="")

    def __str__(self) -> str:
        """Краткое представление конфига для логов."""
        return f"- Booking API: {self.booking_url}"


def load_environment(env: Environment | str) -> EnvironmentConfig:
    """Возвращает конфиг для запрошенного окружения.
    URL берётся из статической таблицы _URLS, секреты — из .env / env vars."""
    env = env if isinstance(env, Environment) else Environment(env.lower())
    return EnvironmentConfig(booking_url=_URLS[env])
