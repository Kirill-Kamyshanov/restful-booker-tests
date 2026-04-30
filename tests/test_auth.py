import pytest
from faker import Faker
from services.restful_booker.auth.assertions import assert_auth


class TestAuth:
    fake = Faker()

    @pytest.mark.parametrize("auth_case, is_positive",[
        ("auth_valid", True),
        ("auth_invalid", False),
        ("auth_empty", False),
        ("auth_without_name", False),
        ("auth_without_password", False)
    ])
    def test_auth(self, api, test_data, auth_case, is_positive):
        """Проверяет авторизацию с валидными/невалидными входными данными"""
        if not is_positive:
            data = api.auth.randomize_dynamic_fields(["username", "password"], test_data["auth"][auth_case], "auth")
            print(data)
            # fields = {"username": self.fake.name(), "password": self.fake.password()}
            # for field in test_data["auth"][auth_case]:
            #     if field in fields.keys():
            #         test_data["auth"][auth_case][field] = fields[field]
        else:
            data = test_data["auth"][auth_case]
        response, validated = api.auth.login(data,is_positive=is_positive)
        # response, validated = api.auth.login(test_data["auth"][auth_case],is_positive=is_positive)
        assert_auth(response, validated)