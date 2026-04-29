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