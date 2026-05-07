import allure
from requests import Response

from services.restful_booker.auth.models.auth import AuthErrorResponse, AuthResponse
from utils.assertions import assert_status_code


def assert_auth(response: Response, validated: AuthResponse | AuthErrorResponse) -> None:
    """Проверка авторизации. Для кейсов с ошибкой проверяется конкретное тело ответа.
    Для error-кейсов статус-код также 200"""
    with allure.step('Проверка авторизации'):
        assert_status_code(response, 200)

        if isinstance(validated, AuthErrorResponse):
            expected_error_body = {"reason": "Bad credentials"} # dict(test_data["auth"][expected_error_body])
            assert validated.reason == expected_error_body["reason"], (
                f"Ожидалось reason={expected_error_body['reason']}, но получено {validated.reason}"
        )
