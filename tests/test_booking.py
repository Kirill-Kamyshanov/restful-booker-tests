import allure
import pytest
from utils.helpers import fake

from services.restful_booker.booking.assertions import (
    assert_booking_created,
    assert_booking_updated_patch,
    assert_booking_updated_put,
    assert_forbidden,
    assert_get_by_id,
    assert_not_found,
)
from services.restful_booker.booking.models.booking import BookingData, UpdateBookingPatchRequest
from utils.assertions import assert_status_code




@pytest.fixture
def test_booking_id(api, cleanup) -> int:
    """Фикстура для создания тестового бронирования. Оставлена здесь, т.к. относится только в этому ресурсу"""
    with allure.step("Создание тестового бронирования"):
        request_data = BookingData().model_dump(mode='json')
        _, validated = api.booking.create(request_data)
        cleanup.append(lambda: api.booking.remove(validated.bookingid))
        return validated.bookingid

@pytest.mark.regression
@allure.feature("Booking")
class TestBooking:

    @pytest.mark.smoke
    @allure.title("Успешное создание бронирования")
    def test_create_booking_successful(self, api):
        with allure.step("Отправка запроса на создание"):
            request_data = BookingData().model_dump(mode='json')
            response, validated = api.booking.create(request_data)
        with allure.step("Проверка успешности создания"):
            assert_booking_created(response, request_data, validated)

    @pytest.mark.xfail(reason="Тест успешно проходит с невалидными датами, но обрабатывает их")
    @allure.title("Создание бронирования с некорректными датами")
    def test_create_booking_with_invalid_dates(self, api, test_data):
        with allure.step("Отправка запроса"):
            request_data = test_data["booking"]["invalid_dates_post"]
            response, _ = api.booking.create(request_data, validate=False)
        with allure.step("Проверка ответа"):
            assert_status_code(response, 400)

    @pytest.mark.parametrize("deleting_field", [
        "firstname",
        "lastname",
        "totalprice",
        "depositpaid",
        "bookingdates",
        "checkin",
        "checkout"
    ])
    @allure.title("Создание бронирования без обязательных полей в запросе")
    def test_create_booking_without_necessary_fields(self, api, deleting_field):
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

    @pytest.mark.smoke
    @allure.title("Успешное удаление бронирования")
    def test_delete_booking_successful(self, api, test_booking_id):
        with allure.step("Отправка запроса"):
            response, _ = api.booking.remove(test_booking_id)
        with allure.step("Проверка ответа"):
            assert_status_code(response, 201)

    @pytest.mark.parametrize("token", [None, "invalid_token"])
    @allure.title("Удаление бронирования без валидного токена")
    def test_delete_booking_with_invalid_creds(self, api, token, test_booking_id, test_data):
        """Проверяет получение ошибки при попытке удалить бронирование
        без токена авторизации / с невалидным токеном"""
        with allure.step("Отправка запроса"):
            token = token if not token else test_data["booking"][token]
            response, _ = api.booking.remove(test_booking_id, headers={"Authorization": token})
        with allure.step("Проверка ответа"):
            assert_forbidden(response)

    @allure.title("Удаление несуществующего бронирования")
    def test_delete_unexisted_booking(self, api, test_data):
        with allure.step("Отправка запроса"):
            response, _ = api.booking.remove(test_data["booking"]["unexisted_id"])
        with allure.step("Проверка ответа"):
            assert_status_code(response, 405)

    @pytest.mark.smoke
    @allure.title("Получение данных о бронировании по id")
    def test_get_booking_by_id(self, api, test_booking_id):
        with allure.step("Отправка запроса"):
            response, _ = api.booking.get_by_id(test_booking_id)
        with allure.step("Проверка ответа"):
            assert_get_by_id(response)

    @allure.title("Получение данных о несуществующем бронировании")
    def test_get_booking_by_unexisted_id(self, api, test_data):
        with allure.step("Отправка запроса"):
            response, _ = api.booking.get_by_id(test_data["booking"]["unexisted_id"], validate=False)
        with allure.step("Проверка ответа"):
            assert_not_found(response)

    @pytest.mark.parametrize("params", [None,
                                        {"firstname": fake.first_name()},
                                        {"lastname": fake.last_name()},
                                        {"checkin": "2026-05-01"},
                                        {"checkout": "2026-05-30"}
                                        ]
                             )
    @allure.title("Получение данных по всем бронированиям")
    def test_get_all_bookings(self, api, params):
        """Получение данных по всем бронированиям без фильтрации / с фильтрацией по квери-параметрам"""
        with allure.step("Отправка запроса"):
            response, _ = api.booking.list(params=params)
        with allure.step("Проверка ответа"):
            assert_status_code(response, 200)

    @pytest.mark.smoke
    @allure.title("Полное успешное обновление данных бронирования методом PUT")
    def test_full_update_booking(self, api, test_booking_id):
        with allure.step("Отправка запроса"):
            new_data = BookingData().model_dump()
            response, validated_put_response = api.booking.update(test_booking_id, new_data, "put")
        with allure.step("Проверка ответа"):
            assert_booking_updated_put(response, BookingData(**new_data), validated_put_response)

    @pytest.mark.parametrize("method", ["put", "patch"])
    @pytest.mark.parametrize("token", [None, "invalid_token"])
    @allure.title("Обновление данных бронирования с невалидным/отсутствующим токеном авторизации")
    def test_update_booking_with_invalid_creds(self, api, test_data, token, method, test_booking_id):
        with allure.step("Отправка запроса"):
            new_data = BookingData().model_dump()
            token = token if not token else test_data["booking"][token]
            response, _ = api.booking.update(test_booking_id, new_data, method, validate=False,
                                             headers={"Authorization": token})
        with allure.step("Проверка ответа"):
            assert_forbidden(response)

    @pytest.mark.parametrize("method", ["put", "patch"])
    @allure.title("Обновление несуществующего бронирования")
    def test_update_unexisted_booking(self, api, method, test_data):
        with allure.step("Отправка запроса"):
            new_data = BookingData().model_dump()
            response, _ = api.booking.update(test_data["booking"]["unexisted_id"], new_data, method, validate=False)
        with allure.step("Проверка ответа"):
            assert_status_code(response, 405)

    @allure.title("Успешное частичное обновление бронирования методом PATCH")
    def test_patch_update_booking(self, api, test_data, test_booking_id):
        with allure.step("Отправка запроса"):
            new_data = UpdateBookingPatchRequest(**test_data["booking"]["valid_patch"]).model_dump(exclude_none=True)
            response, validated_patch_response = api.booking.update(test_booking_id, new_data, "patch")
        with allure.step("Проверка ответа"):
            assert_booking_updated_patch(response, new_data, validated_patch_response)
