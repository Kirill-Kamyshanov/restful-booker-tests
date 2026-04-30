import pytest

from services.restful_booker.auth.assertions import assert_auth


class TestAuth:

    @pytest.mark.parametrize("auth_case, is_positive",[
        ("auth_valid", True),
        ("auth_invalid", False),
        ("auth_empty", False),
        ("auth_without_name", False),
        ("auth_without_password", False)
    ])
    def test_auth(self, api, test_data, auth_case, is_positive):
        """Проверяет авторизацию с валидными/невалидными входными данными"""
        fields = ["username", "password"]
        response, validated = api.auth.login(test_data["auth"][auth_case],is_positive=is_positive)
        assert_auth(response, validated)