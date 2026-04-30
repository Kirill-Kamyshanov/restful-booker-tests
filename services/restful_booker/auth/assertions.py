from requests import Response

from services.restful_booker.auth.models.auth import AuthErrorResponse, AuthResponse
from utils.assertions import assert_status_code

def assert_auth(response: Response, validated: AuthResponse | AuthErrorResponse) -> None:
    """Проверка авторизации"""
    assert_status_code(response, 200)
    # print(validated)

    if isinstance(validated, AuthErrorResponse):
        expected_error_body = {"reason": "Bad credentials"}
        assert validated.reason == expected_error_body["reason"], (
            f"Ожидалось reason={expected_error_body['reason']}, но получено {validated.reason}"
        )