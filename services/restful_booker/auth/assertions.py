import allure
from requests import Response

from services.restful_booker.auth.models.auth import AuthErrorResponse, AuthResponse
from utils.assertions import assert_status_code


def assert_auth_successful(response: Response, validated: AuthResponse) -> None:
    """Проверка успешной авторизации. validated в настоящее время не используется,
    т.к. нет особой логики при проверке ответа. Оставил из-за наличия в ТЗ"""
    with allure.step('Проверка успешной авторизации'):
        assert_status_code(response, 200)



def assert_auth_failed(response: Response, expected_error: AuthErrorResponse) -> None:
    """Проверка, что авторизация не была пройдена. Статус-код для error-кейсов 200"""

    with allure.step('Проверка отказа в доступе при авторизации'):
        assert_status_code(response, 200)
        actual_response = response.json()

        assert  actual_response["reason"] == expected_error.reason, (
            f"Ожидалось reason={expected_error.reason}, но получено {actual_response["reason"]}"
    )