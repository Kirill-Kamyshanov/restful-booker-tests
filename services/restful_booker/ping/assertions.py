import allure
from requests import Response

from utils.assertions import assert_status_code, assert_response_text


def assert_ping(response: Response) -> None:
    """Проверяет успешное получение ресурса: статус 201 и совпадение текста."""
    with allure.step("Проверка получения ресурса: статус-код и текст"):
        expected_text = "Created"
        assert_response_text(response, expected_text)
        assert_status_code(response, 201)
