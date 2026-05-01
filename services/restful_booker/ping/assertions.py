from requests import Response
from utils.assertions import assert_status_code, assert_text


def assert_ping(response: Response, response_text: str ) -> None:
    """Проверяет успешное получение ресурса: статус 201 и совпадение текста."""
    expected_text = "Created"
    assert_text(response, expected_text)
    assert_status_code(response, 201)