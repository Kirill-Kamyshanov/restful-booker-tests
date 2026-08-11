import allure
import pytest

from services.restful_booker.auth.assertions import assert_auth_failed, assert_auth_successful
from services.restful_booker.auth.models.auth import AuthErrorResponse, AuthRequest



@pytest.mark.regression
@allure.feature("Authentication")
class TestAuth:

    @pytest.mark.smoke
    @allure.title("Успешная авторизация")
    def test_auth_positive(self, api, test_data):
        """Faker не используется, т.к. валидной считается всего одна пара username/password"""

        with allure.step("Подготовка тестовых данных"):
            auth_data = AuthRequest(**test_data["auth"]["auth_valid"]).model_dump()

        with allure.step("Отправка запроса на авторизацию"):
            response, validated = api.auth.login(auth_data)

        with allure.step("Проверка результата"):
            assert_auth_successful(response, validated)

    @pytest.mark.smoke
    @pytest.mark.parametrize("auth_case", [
        "auth_invalid",
        "auth_empty",
        "auth_without_name",
        "auth_without_password"
    ])
    @allure.title("Авторизация с невалидными входными данными")
    def test_auth_negative(self, api, test_data, auth_case):

        with allure.step("Подготовка тестовых данных"):
            expected_response_body = AuthErrorResponse(**test_data["auth"]["auth_error_response"])
            request_body = test_data["auth"][auth_case]

        with allure.step("Отправка запроса на авторизацию"):
            response, _ = api.auth.login(request_body, validate=False)

        with allure.step("Проверка результата"):
            assert_auth_failed(response, expected_response_body)
