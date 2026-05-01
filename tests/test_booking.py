from services.restful_booker.booking.assertions import assert_creation, assert_code_and_text, assert_get_by_id
from services.restful_booker.booking.models.booking import BookingDataRequest
from utils.assertions import assert_status_code
import pytest




class TestBooking:


    def test_create_booking_successful(self, api, cleanup):
        """Создание бронирования с валидными входными данными"""
        request_data = BookingDataRequest().model_dump(mode='json')
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
        request_data = BookingDataRequest().model_dump(mode='json')

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
        request_data = BookingDataRequest().model_dump(mode='json')
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
        request_data = BookingDataRequest().model_dump(mode='json')
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
        request_data = BookingDataRequest().model_dump(mode='json')
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



# Получение информации о бронировании:
# Получение списка всех бронирований
# Фильтрация бронирований по имени
# Фильтрация бронирований по фамилии
# Фильтрация бронирований по дате заезда
# Фильтрация бронирований по дате выезда


# Обновление бронирования:
# Полное успешное обновление бронирования
# Частичное успешное обновление бронирования
# Обновление бронирования без токена авторизации
# Обновление бронирования с неверным токеном
# Обновление несуществующего бронирования



