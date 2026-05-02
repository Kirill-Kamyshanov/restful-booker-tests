import pytest
from faker import Faker

from services.restful_booker.auth.assertions import assert_auth
from services.restful_booker.auth.models.auth import AuthRequest


class TestAuth:
    fake = Faker()

    @pytest.mark.parametrize("auth_case, is_positive", [
        ("auth_valid", True),
        ("auth_invalid", False),
        ("auth_empty", False),
        ("auth_without_name", False),
        ("auth_without_password", False)
    ])
    def test_auth(self, api, test_data, auth_case, is_positive):
        """Проверяет авторизацию с валидными/невалидными входными данными"""
        if not is_positive:
            data = test_data["auth"][auth_case]
            fields = {"username": self.fake.name(), "password": self.fake.password()}
            for field in data:
                if field in fields:
                    test_data["auth"][auth_case][field] = fields[field]
        else:
            data = AuthRequest(**test_data["auth"][auth_case]).model_dump()
        response, validated = api.auth.login(data, is_positive=is_positive)
        assert_auth(response, validated)
