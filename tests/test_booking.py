import faker
from faker import Faker

from services.restful_booker.booking.assertions import assert_creation, assert_code_and_text, assert_get_by_id, \
    assert_put_booking, assert_patch_booking
from services.restful_booker.booking.models.booking import BookingData, UpdateBookingPatchRequest
from utils.assertions import assert_status_code
import pytest

fake = Faker()


class TestBooking:


    def test_create_booking_successful(self, api, cleanup):
        """Создание бронирования с валидными входными данными"""
        request_data = BookingData().model_dump(mode='json')
        print(type(request_data))
        print(request_data)

        response, validated = api.booking.create(request_data)
        cleanup.append(lambda: api.booking.remove(validated.bookingid))
        print(f"Юзер удалён {validated.bookingid}")
        print(response)
        print(type(validated))
        # print(validated.model_dump(mode='json'))

        assert_creation(response,
                        validated,
                        request_data["firstname"],
                        request_data["lastname"],
                        request_data["totalprice"],
                        request_data["depositpaid"],
                        request_data["bookingdates"],
                        request_data["additionalneeds"]
                        )



    # Тут поведение системы специфическое. Ждал код 400, получил 200 с некорректными датами. Но они были обработаны
    # Оставил тест как есть. В реальном проекте уточнил бы требования
    def test_create_booking_with_invalid_dates(self, api, test_data):
        """Создание бронирования с некорректными датами"""
        request_data = test_data["booking"]["invalid_dates_post"]
        print(type(request_data))
        print(request_data)

        response, validated = api.booking.create(request_data, validate=False)
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
        # print(type(request_data))
        # print(request_data)

        response, validated = api.booking.create(request_data, validate=False)
        assert_status_code(response, 500)




    def test_delete_booking_successful(self, api):
        """Проверяет успешное удаление бронирования"""
        # создание
        request_data = BookingData().model_dump(mode='json')
        _, validated = api.booking.create(request_data)

        # удаление
        response, text = api.booking.remove(validated.bookingid)
        # проверка удаления
        assert_code_and_text(response, 201, "Created")
        # print(text)
        # print(response)



    @pytest.mark.parametrize("token", [None, "battletoads2"])
    def test_delete_booking_with_invalid_creds(self, api, token, cleanup):
        """Проверяет получение ошибки при попытке удалить бронирование
        без токена авторизации / с невалидным токеном"""
        # создание
        request_data = BookingData().model_dump(mode='json')
        _, validated = api.booking.create(request_data)
        cleanup.append(lambda: api.booking.remove(validated.bookingid))
        # удаление
        response, text = api.booking.remove(validated.bookingid, headers={"Authorization": token})
        assert_code_and_text(response, 403, "Forbidden")



    def test_delete_unexisted_booking(self, api, cleanup):
        """Проверка удаления несуществующего бронирования"""
        unexisted_id = 9999999
        response, text = api.booking.remove(unexisted_id)
        assert_code_and_text(response, 405, "Method Not Allowed")


    def test_get_booking_by_id(self, api, cleanup):
        """Успешное получение данных о бронировании"""
        # создание
        request_data = BookingData().model_dump(mode='json')
        _, validated = api.booking.create(request_data)
        # print(validated.bookingid)
        cleanup.append(lambda: api.booking.remove(validated.bookingid))
        # получение
        response, validated2 = api.booking.get_by_id(validated.bookingid)
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
        # print(params)
        response, validated = api.booking.get_list_bookings(params=params)
        assert_status_code(response, 200)



    def test_full_update_booking(self, api, cleanup):
        """Проверка успешного полного обновления данных бронирования методом PUT"""
        # создание
        request_data = BookingData().model_dump(mode='json')
        _, validated_response = api.booking.create(request_data)
        booking_id = validated_response.bookingid
        cleanup.append(lambda: api.booking.remove(booking_id))
        # обновление
        new_data = BookingData().model_dump()
        # print(BookingData(**new_data))
        response, validated_put_response = api.booking.update_booking(booking_id, new_data, "put")
        # проверка
        # print(validated_put_response)
        assert_put_booking(response, BookingData(**new_data), validated_put_response)


    @pytest.mark.parametrize("method", ["put", "patch"])
    @pytest.mark.parametrize("token", [None, "battletoads2"])
    def test_update_booking_with_invalid_creds(self, api, cleanup, test_data, token, method):
        """Проверка полного/частичного обновления данных бронирования с невалидным/отсутствующим токеном"""
        # создание
        request_data = BookingData().model_dump(mode='json')
        _, validated_response = api.booking.create(request_data)
        booking_id = validated_response.bookingid
        cleanup.append(lambda: api.booking.remove(booking_id))
        # обновление
        new_data = BookingData().model_dump()
        # print(BookingData(**new_data))
        response, text_response = api.booking.update_booking(booking_id, new_data, method, validate=False,
                                                             headers={"Authorization": token})
        # проверка
        # print(validated_put_response)
        assert_code_and_text(response, 403, text_response)



    @pytest.mark.parametrize("method", ["put", "patch"])
    def test_update_unexisted_booking(self, api, cleanup, method):
        """Проверка полного/частичного обновления несуществующего бронирования"""
        # создание
        unexisted_id = 9999999
        # обновление
        new_data = BookingData().model_dump()
        # print(BookingData(**new_data))
        response, validated_put_response = api.booking.update_booking(unexisted_id, new_data, method, validate=False)
        # проверка
        # print(validated_put_response)
        assert_code_and_text(response, 405, "Method Not Allowed")



    def test_patch_update_booking(self, api, cleanup, test_data):
        """Проверка успешного частичного обновления данных бронирования методом PATCH"""
        # создание
        request_data = BookingData().model_dump(mode='json')
        _, validated_response = api.booking.create(request_data)
        booking_id = validated_response.bookingid
        cleanup.append(lambda: api.booking.remove(booking_id))
        # обновление
        new_data = UpdateBookingPatchRequest(**test_data["booking"]["valid_patch"]).model_dump(exclude_none=True)
        print(new_data)
        response, validated_patch_response = api.booking.update_booking(booking_id, new_data, "patch")
        # print(response)
        print(validated_patch_response)
        assert_patch_booking(response, new_data, validated_patch_response)


# Обновление бронирования:
# Частичное успешное обновление бронирования +
# Обновление бронирования без токена авторизации +-
# Обновление бронирования с неверным токеном +-



