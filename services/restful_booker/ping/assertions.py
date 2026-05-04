from requests import Response

from utils.assertions import assert_response_text, assert_status_code


def assert_ping(response: Response) -> None:
    """Проверяет успешное получение ресурса: статус 201 и совпадение текста."""
    expected_text = "Created"
    assert_response_text(response, expected_text)
    assert_status_code(response, 201)
