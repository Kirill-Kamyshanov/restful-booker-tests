from requests import Response
from utils.assertions import assert_status_code


def assert_ping(response: Response, response_text: str ) -> None:
    """Проверяет успешное получение ресурса: статус 201 и совпадение текста."""
    expected_text = "Created"
    assert_status_code(response, 201)
    assert response_text == expected_text, f"Ожидался текст {expected_text}, получен {response_text}"
