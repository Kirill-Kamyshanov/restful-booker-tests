from services.restful_booker.ping.assertions import assert_ping


class TestPing:

    def test_ping(self, api):
        """Проверка доступности API через пинг-запрос"""
        response, text = api.ping.ping()
        assert_ping(response, text)