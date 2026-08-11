import json
import warnings
from collections.abc import Callable, Generator
from pathlib import Path

import pytest

from config.environments import Environment, EnvironmentConfig, load_environment
from services.restful_booker.api import RestfulBookerApi


def pytest_addoption(parser: pytest.Parser) -> None:
    """Регистрация кастомной CLI опции --env для запуска тестов в разных окружениях"""
    parser.addoption("--env", action="store", default="dev", help="Окружение для запуска тестов (dev/stage)")


@pytest.fixture(scope="session")
def env(request: pytest.FixtureRequest) -> Environment:
    """Возвращает выбранное окружение из CLI-опции --env."""
    env_name = request.config.getoption("--env")
    try:
        return Environment(env_name.lower())
    except ValueError as exc:
        raise ValueError(f"Некорректное окружение: {env_name}. Используйте одно из: dev/stage") from exc


def pytest_configure(config: pytest.Config) -> None:
    """Хук контролирует переданное при запуске окружение. При невалидном значении --env тесты не запустятся.
    Выполняется после парсинга аргументов, но до начала сбора тестов.
    'env_name' берётся из переданного в CLI/дефолтное
    'allowed' создаётся из доступных окружений в классе Environment"""
    env_name = config.getoption("--env")
    allowed = [x.value for x in Environment]
    if env_name.lower() not in allowed:
        pytest.exit(f"Неизвестное окружение: {env_name}. Используйте --env=dev или --env=stage")


@pytest.fixture(scope="session")
def data_for_generate_auth_token(env: Environment) -> dict:
    """Возвращает данные для генерации auth-токена,
    который принимается в хедере Cookie в качестве альтернативы хедеру Authorization"""
    config = load_environment(env)
    return {"username": f"{config.booker_username}", "password": f"{config.booker_password}"}


@pytest.fixture(scope="session")
def env_config(env: Environment) -> EnvironmentConfig:
    """Загружает конфиг текущего окружения (URL + секреты)."""
    config = load_environment(env)
    print(f"\nОкружение: {env}\n{config}\n")
    return config


@pytest.fixture(scope="session")
def test_data(env: Environment) -> dict:
    """Загружает тестовые данные окружения из test_data/{env}.json"""
    path = Path(__file__).parent / "test_data" / f"{env.value}.json"
    with path.open(encoding="utf-8") as f:
        return json.load(f)


@pytest.fixture
def api(env_config: EnvironmentConfig) -> RestfulBookerApi:
    """Главный фасад над сервисом reqres.in: api.ping / api.booking / api.auth."""
    return RestfulBookerApi(env_config)


@pytest.fixture
def cleanup() -> Generator[list[Callable[[], None]], None, None]:
    """Список действий очистки, которые выполнятся после теста (в обратном порядке).

    Сразу после создания сущности тест добавляет действие удаления:
        cleanup.append(lambda: api.users.remove(user_id))
    После теста все действия выполняются с конца списка. Ошибка одного не прерывает остальные.
    """
    tasks: list[Callable[[], None]] = []
    yield tasks
    errors: list[Exception] = []
    for task in reversed(tasks):
        try:
            task()
        except Exception as exc:
            errors.append(exc)
    if errors:
        warnings.warn(f"Cleanup errors: {errors}", stacklevel=2)
