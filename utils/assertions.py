import allure
from requests import Response


def assert_status_code(response: Response, expected_code: int) -> None:
    """Проверка, что полученный статус-код соответствует ожидаемому"""
    with allure.step("Проверка соответствия статус-кода ожидаемому"):
        assert response.status_code == expected_code, (
            f"Ожидался статус-код {expected_code}, но получен {response.status_code} : {response.text}"
        )


def assert_response_text(response: Response, expected_text: str) -> None:
    """Проверка, что полученный текст ответа соответствует ожидаемому"""
    with allure.step("Проверка соответствия полученного текста в ответе ожидаемому"):
        assert response.text == expected_text, f"Ожидался текст {expected_text}, но получен {response.text}"
