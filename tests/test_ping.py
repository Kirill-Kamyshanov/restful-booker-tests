import allure
import pytest

from services.restful_booker.ping.assertions import assert_ping


@allure.feature("Ping")
class TestPing:
    @pytest.mark.regression
    @pytest.mark.smoke
    @allure.title("Проверка доступности API через PING-запрос")
    def test_ping(self, api):
        """Проверка доступности API через пинг-запрос"""
        with allure.step("Отправка запроса"):
            response, _ = api.ping.ping()
        with allure.step("Проверка результата"):
            assert_ping(response)
