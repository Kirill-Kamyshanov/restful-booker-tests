import allure
import pytest
from faker import Faker

from services.restful_booker.auth.assertions import assert_auth
from services.restful_booker.auth.models.auth import AuthRequest


@allure.feature("Authentication")
class TestAuth:
    fake = Faker()

    @pytest.mark.regression
    @pytest.mark.smoke
    @pytest.mark.parametrize("auth_case, is_positive", [
        ("auth_valid", True),
        ("auth_invalid", False),
        ("auth_empty", False),
        ("auth_without_name", False),
        ("auth_without_password", False)
    ])
    @allure.testcase("https://jira.example.com/TC-1", "TC-1")
    @allure.title("Авторизация")
    def test_auth(self, api, test_data, auth_case, is_positive):
        """Проверяет авторизацию с валидными/невалидными входными данными"""
        with allure.step("Подготовка тестовых данных"):
            if not is_positive:
                data = dict(test_data["auth"][auth_case])
                fields = {"username": self.fake.name(), "password": self.fake.password()}
                for field in data:
                    if field in fields:
                        data[field] = fields[field]
            else:
                data = AuthRequest(**test_data["auth"][auth_case]).model_dump()
        with allure.step("Отправка запроса на авторизацию"):
            response, validated = api.auth.login(data, is_positive=is_positive)
        with allure.step("Проверка результата"):
            assert_auth(response, validated)
