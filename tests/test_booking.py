import allure
import pytest
from faker import Faker

from services.restful_booker.booking.assertions import (
    assert_booking_created,
    assert_booking_updated_patch,
    assert_booking_updated_put,
    assert_code_and_text,
    assert_forbidden,
    assert_get_by_id,
    assert_not_found,
)
from services.restful_booker.booking.models.booking import BookingData, UpdateBookingPatchRequest
from utils.assertions import assert_status_code

fake = Faker()


@pytest.fixture
def test_booking_id(api, cleanup) -> int:
    """Фикстура для создания тестового бронирования. Оставлена здесь, т.к. относится только в этому ресурсу"""
    with allure.step("Создание тестового бронирования"):
        request_data = BookingData().model_dump(mode='json')
        _, validated = api.booking.create(request_data)
        cleanup.append(lambda: api.booking.remove(validated.bookingid))
        return validated.bookingid


@allure.feature("Booking")
class TestBooking:

    @pytest.mark.regression
    @pytest.mark.smoke
    @allure.testcase("https://jira.example.com/TC-3", "TC-3")
    @allure.title("Успешное создание бронирования")
    def test_create_booking_successful(self, api):
        """Создание бронирования с валидными входными данными"""
        with allure.step("Отправка запроса на создание"):
            request_data = BookingData().model_dump(mode='json')
            response, validated = api.booking.create(request_data)
        with allure.step("Проверка успешности создания"):
            assert_booking_created(response, request_data, validated)

    # Тут поведение системы специфическое. Ждал код 400, получил 200 с некорректными датами. Но они были обработаны
    # Оставил тест как есть. В реальном проекте уточнил бы требования
    @pytest.mark.regression
    @allure.testcase("https://jira.example.com/TC-4", "TC-4")
    @allure.title("Создание бронирования с некорректными датами")
    def test_create_booking_with_invalid_dates(self, api, test_data):
        """Создание бронирования с некорректными датами"""
        with allure.step("Отправка запроса"):
            request_data = test_data["booking"]["invalid_dates_post"]
            response, _ = api.booking.create(request_data, validate=False)
        with allure.step("Проверка ответа"):
            assert_status_code(response, 400)

    # тут баг - успешное создание без поля additionalneeds (обязательное)
    @pytest.mark.regression
    @pytest.mark.parametrize("deleting_field", [
        "firstname",
        "lastname",
        "totalprice",
        "depositpaid",
        "bookingdates",
        "checkin",
        "checkout",
        "additionalneeds"
    ])
    @allure.testcase("https://jira.example.com/TC-5", "TC-5")
    @allure.title("Создание бронирования без обязательных полей в запросе")
    def test_create_booking_without_necessary_fields(self, api, deleting_field):
        """Создание бронирования без обязательных полей в запросе"""
        with allure.step("Подготовка тестовых данных"):
            request_data = BookingData().model_dump(mode='json')

            if deleting_field == "checkin" or deleting_field == "checkout":
                del request_data["bookingdates"][deleting_field]
            else:
                del request_data[deleting_field]
        with allure.step("Отправка запроса"):
            response, _ = api.booking.create(request_data, validate=False)
        with allure.step("Проверка ответа"):
            assert_status_code(response, 500)

    @pytest.mark.regression
    @pytest.mark.smoke
    @allure.testcase("https://jira.example.com/TC-6", "TC-6")
    @allure.title("Успешное удаление бронирования")
    def test_delete_booking_successful(self, api, test_booking_id):
        """Проверяет успешное удаление бронирования"""
        with allure.step("Отправка запроса"):
            response, _ = api.booking.remove(test_booking_id)
        with allure.step("Проверка ответа"):
            assert_code_and_text(response, 201, "Created")

    @pytest.mark.regression
    @pytest.mark.parametrize("token", [None, "battletoads2"])
    @allure.testcase("https://jira.example.com/TC-7", "TC-7")
    @allure.title("Удаление бронирования без валидного токена")
    def test_delete_booking_with_invalid_creds(self, api, token, test_booking_id):
        """Проверяет получение ошибки при попытке удалить бронирование
        без токена авторизации / с невалидным токеном"""
        with allure.step("Отправка запроса"):
            response, _ = api.booking.remove(test_booking_id, headers={"Authorization": token})
        with allure.step("Проверка ответа"):
            assert_forbidden(response)

    @pytest.mark.regression
    @allure.testcase("https://jira.example.com/TC-8", "TC-8")
    @allure.title("Удаление несуществующего бронирования")
    def test_delete_unexisted_booking(self, api):
        """Проверка удаления несуществующего бронирования"""
        unexisted_id = 9999999
        with allure.step("Отправка запроса"):
            response, _ = api.booking.remove(unexisted_id)
        with allure.step("Проверка ответа"):
            assert_code_and_text(response, 405, "Method Not Allowed")

    @pytest.mark.regression
    @pytest.mark.smoke
    @allure.testcase("https://jira.example.com/TC-9", "TC-9")
    @allure.title("Получение данных о бронировании по id")
    def test_get_booking_by_id(self, api, test_booking_id):
        """Успешное получение данных о бронировании"""
        with allure.step("Отправка запроса"):
            response, _ = api.booking.get_by_id(test_booking_id)
        with allure.step("Проверка ответа"):
            assert_get_by_id(response)

    @pytest.mark.regression
    @allure.testcase("https://jira.example.com/TC-10", "TC-10")
    @allure.title("Получение данных о несуществующем бронировании")
    def test_get_booking_by_unexisted_id(self, api):
        """Попытка получить данные по несуществующему бронированию"""
        unexisted_id = 9999999
        with allure.step("Отправка запроса"):
            response, _ = api.booking.get_by_id(unexisted_id, validate=False)
        with allure.step("Проверка ответа"):
            assert_not_found(response)

    @pytest.mark.regression
    @pytest.mark.parametrize("params", [None,
                                        {"firstname": fake.first_name()},
                                        {"lastname": fake.last_name()},
                                        {"checkin": "2026-05-01"},
                                        {"checkout": "2026-05-30"}
                                        ]
                             )
    @allure.testcase("https://jira.example.com/TC-11", "TC-11")
    @allure.title("Получение данных по всем бронированиям")
    def test_get_all_bookings(self, api, params):
        """Получение данных по всем бронированиям без фильтрации / с фильтрацией по квери-параметрам"""
        with allure.step("Отправка запроса"):
            response, _ = api.booking.list(params=params)
        with allure.step("Проверка ответа"):
            assert_status_code(response, 200)

    @pytest.mark.regression
    @pytest.mark.smoke
    @allure.testcase("https://jira.example.com/TC-12", "TC-12")
    @allure.title("Полное успешное обновление данных бронирования методом PUT")
    def test_full_update_booking(self, api, test_booking_id):
        """Проверка успешного полного обновления данных бронирования методом PUT"""
        with allure.step("Отправка запроса"):
            new_data = BookingData().model_dump()
            response, validated_put_response = api.booking.update(test_booking_id, new_data, "put")
        with allure.step("Проверка ответа"):
            assert_booking_updated_put(response, BookingData(**new_data), validated_put_response)

    @pytest.mark.regression
    @pytest.mark.parametrize("method", ["put", "patch"])
    @pytest.mark.parametrize("token", [None, "battletoads2"])
    @allure.testcase("https://jira.example.com/TC-13", "TC-13")
    @allure.title("Удаление бронирования с невалидным/отсутствующим токеном авторизации")
    def test_update_booking_with_invalid_creds(self, api, test_data, token, method, test_booking_id):
        """Проверка полного/частичного обновления данных бронирования с невалидным/отсутствующим токеном"""
        with allure.step("Отправка запроса"):
            new_data = BookingData().model_dump()
            response, _ = api.booking.update(test_booking_id, new_data, method, validate=False,
                                             headers={"Authorization": token})
        with allure.step("Проверка ответа"):
            assert_forbidden(response)

    @pytest.mark.regression
    @pytest.mark.parametrize("method", ["put", "patch"])
    @allure.testcase("https://jira.example.com/TC-14", "TC-14")
    @allure.title("Обновление несуществующего бронирования")
    def test_update_unexisted_booking(self, api, method):
        """Проверка полного/частичного обновления несуществующего бронирования"""
        unexisted_id = 9999999
        with allure.step("Отправка запроса"):
            new_data = BookingData().model_dump()
            response, _ = api.booking.update(unexisted_id, new_data, method, validate=False)
        with allure.step("Проверка ответа"):
            assert_code_and_text(response, 405, "Method Not Allowed")

    @pytest.mark.regression
    @allure.testcase("https://jira.example.com/TC-15", "TC-15")
    @allure.title("Успешное частичное обновление бронирования методом PATCH")
    def test_patch_update_booking(self, api, test_data, test_booking_id):
        """Проверка успешного частичного обновления данных бронирования методом PATCH"""
        with allure.step("Отправка запроса"):
            new_data = UpdateBookingPatchRequest(**test_data["booking"]["valid_patch"]).model_dump(exclude_none=True)
            response, validated_patch_response = api.booking.update(test_booking_id, new_data, "patch")
        with allure.step("Проверка ответа"):
            assert_booking_updated_patch(response, new_data, validated_patch_response)
