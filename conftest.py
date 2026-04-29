import pytest

from config.environments import Environment


def pytest_addoption(parser: pytest.Parser) -> None:
    """Регистрация кастомной CLI опции --env для запуска тестов в разных окружениях"""
    parser.addoption(
        "--env",
        action="store",
        default="dev",
        help="Окружение для запуска тестов (dev/prod)"
    )

@pytest.fixture(scope="session")
def env() -> Environment:
    """Возвращает выбранное окружение из CLI-опции --env."""
    env_name = request.config.getoption("--env")
    print(Environment(env_name.lower()))