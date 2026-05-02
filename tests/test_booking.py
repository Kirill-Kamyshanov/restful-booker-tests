import pytest
from faker import Faker

from services.restful_booker.booking.assertions import (
    assert_code_and_text,
    assert_creation,
    assert_get_by_id,
    assert_patch_booking,
    assert_put_booking,
)
from services.restful_booker.booking.models.booking import BookingData, UpdateBookingPatchRequest
from utils.assertions import assert_status_code

fake = Faker()


@pytest.fixture
def test_user_id(api) -> int:
    """Фикстура для создания тестового юзера. Оставлена здесь, т.к. относится только в этому ресурсу"""
    request_data = BookingData().model_dump(mode='json')
    _, validated = api.booking.create(request_data)
    return validated.bookingid


class TestBooking:

    def test_create_booking_successful(self, api, cleanup):
        """Создание бронирования с валидными входными данными"""
        request_data = BookingData().model_dump(mode='json')
        response, validated = api.booking.create(request_data)
        cleanup.append(lambda: api.booking.remove(validated.bookingid))

        assert_creation(response, request_data, validated)

    # Тут поведение системы специфическое. Ждал код 400, получил 200 с некорректными датами. Но они были обработаны
    # Оставил тест как есть. В реальном проекте уточнил бы требования
    def test_create_booking_with_invalid_dates(self, api, test_data):
        """Создание бронирования с некорректными датами"""
        request_data = test_data["booking"]["invalid_dates_post"]

        response, _ = api.booking.create(request_data, validate=False)
        assert_status_code(response, 400)

    # тут баг - успешное создание без поля additionalneeds (обязательное)
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
    def test_create_booking_without_necessary_fields(self, api, deleting_field):
        """Создание бронирования без обязательных полей в запросе"""
        request_data = BookingData().model_dump(mode='json')

        if deleting_field == "checkin" or deleting_field == "checkout":
            del request_data["bookingdates"][deleting_field]
        else:
            del request_data[deleting_field]

        response, _ = api.booking.create(request_data, validate=False)
        assert_status_code(response, 500)

    def test_delete_booking_successful(self, api, test_user_id):
        """Проверяет успешное удаление бронирования"""

        # удаление
        response, _ = api.booking.remove(test_user_id)
        # проверка удаления
        assert_code_and_text(response, 201, "Created")

    @pytest.mark.parametrize("token", [None, "battletoads2"])
    def test_delete_booking_with_invalid_creds(self, api, token, cleanup, test_user_id):
        """Проверяет получение ошибки при попытке удалить бронирование
        без токена авторизации / с невалидным токеном"""
        # создание
        cleanup.append(lambda: api.booking.remove(test_user_id))
        # удаление
        response, _ = api.booking.remove(test_user_id, headers={"Authorization": token})
        assert_code_and_text(response, 403, "Forbidden")

    def test_delete_unexisted_booking(self, api, cleanup):
        """Проверка удаления несуществующего бронирования"""
        unexisted_id = 9999999
        response, _ = api.booking.remove(unexisted_id)
        assert_code_and_text(response, 405, "Method Not Allowed")

    def test_get_booking_by_id(self, api, cleanup, test_user_id):
        """Успешное получение данных о бронировании"""
        # создание
        cleanup.append(lambda: api.booking.remove(test_user_id))
        # получение
        response, validated2 = api.booking.get_by_id(test_user_id)
        # проверка получения (тело ответа было валидировано при получении. пока оставил в ассерте ниже)
        assert_get_by_id(response, validated2)

    def test_get_booking_by_unexisted_id(self, api, cleanup):
        """Попытка получить данные по несуществующему бронированию"""
        unexisted_id = 9999999

        # получение
        response, _ = api.booking.get_by_id(unexisted_id, validate=False)
        assert_code_and_text(response, 404, "Not Found")

    @pytest.mark.parametrize("params", [None,
                                        {"firstname": fake.first_name()},
                                        {"lastname": fake.last_name()},
                                        {"checkin": "2026-05-01"},
                                        {"checkout": "2026-05-30"}
                                        ]
                             )
    def test_get_all_bookings(self, api, params):
        """Получение данных по всем бронированиям без фильтрации / с фильтрацией по квери-параметрам"""
        response, _ = api.booking.get_list_bookings(params=params)
        assert_status_code(response, 200)

    def test_full_update_booking(self, api, cleanup, test_user_id):
        """Проверка успешного полного обновления данных бронирования методом PUT"""
        # создание

        cleanup.append(lambda: api.booking.remove(test_user_id))
        # обновление
        new_data = BookingData().model_dump()
        response, validated_put_response = api.booking.update_booking(test_user_id, new_data, "put")
        # проверка
        assert_put_booking(response, BookingData(**new_data), validated_put_response)

    @pytest.mark.parametrize("method", ["put", "patch"])
    @pytest.mark.parametrize("token", [None, "battletoads2"])
    def test_update_booking_with_invalid_creds(self, api, cleanup, test_data, token, method, test_user_id):
        """Проверка полного/частичного обновления данных бронирования с невалидным/отсутствующим токеном"""
        # создание
        cleanup.append(lambda: api.booking.remove(test_user_id))
        # обновление
        new_data = BookingData().model_dump()
        response, text_response = api.booking.update_booking(test_user_id, new_data, method, validate=False,
                                                             headers={"Authorization": token})
        # проверка
        assert_code_and_text(response, 403, text_response)

    @pytest.mark.parametrize("method", ["put", "patch"])
    def test_update_unexisted_booking(self, api, cleanup, method):
        """Проверка полного/частичного обновления несуществующего бронирования"""
        # создание
        unexisted_id = 9999999
        # обновление
        new_data = BookingData().model_dump()
        response, _ = api.booking.update_booking(unexisted_id, new_data, method, validate=False)
        # проверка
        assert_code_and_text(response, 405, "Method Not Allowed")

    def test_patch_update_booking(self, api, cleanup, test_data, test_user_id):
        """Проверка успешного частичного обновления данных бронирования методом PATCH"""
        # создание

        cleanup.append(lambda: api.booking.remove(test_user_id))
        # обновление
        new_data = UpdateBookingPatchRequest(**test_data["booking"]["valid_patch"]).model_dump(exclude_none=True)
        response, validated_patch_response = api.booking.update_booking(test_user_id, new_data, "patch")
        # проверка обновления
        assert_patch_booking(response, new_data, validated_patch_response)
