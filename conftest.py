import json
from pathlib import Path

import pytest

from config.environments import Environment, EnvironmentConfig, load_environment


def pytest_addoption(parser: pytest.Parser) -> None:
    """Регистрация кастомной CLI опции --env для запуска тестов в разных окружениях"""
    parser.addoption(
        "--env",
        action="store",
        default="dev",
        help="Окружение для запуска тестов (dev/prod)"
    )


@pytest.fixture(scope="session")
def env(request: pytest.FixtureRequest) -> Environment:
    """Возвращает выбранное окружение из CLI-опции --env."""
    env_name = request.config.getoption("--env")
    try:
        return Environment(env_name.lower())
    except ValueError as exc:
        raise ValueError(f"Некорректное окружение: {env_name}. Используйте одно из: dev/stage") from exc


@pytest.fixture(scope="session")
def env_config(env: Environment) -> EnvironmentConfig:
    """Загружает конфиг текущего окружения (URL + секреты)."""
    config = load_environment(env)
    print(f"\nОкружение: {env}\n{config}\n")
    return config


@pytest.fixture(scope="session")
def test_data(env: Environment) -> dict:
    """Загружает тестовые данные окружения из test_data/{env}.json"""
    path = Path(__file__).parent / "test_data" /f"{env}.json"
    with path.open(encoding="utf-8") as f:
        return json.load(f)
