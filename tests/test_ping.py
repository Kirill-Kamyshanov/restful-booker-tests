import allure
import pytest

from services.restful_booker.ping.assertions import assert_ping


@pytest.mark.regression
@allure.feature("Ping")
class TestPing:
    @pytest.mark.smoke
    @allure.title("Проверка доступности API через PING-запрос")
    def test_ping(self, api):
        with allure.step("Отправка запроса"):
            response, _ = api.ping.ping()
        with allure.step("Проверка результата"):
            assert_ping(response)
