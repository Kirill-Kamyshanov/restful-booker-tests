from services.restful_booker.booking.assertions import assert_creation
from services.restful_booker.booking.models.booking import BookingDataRequest
from utils.assertions import assert_status_code
import pytest




class TestBooking:


    def test_create_booking_successful(self, api):
        """Создание бронирования с валидными входными данными"""
        request_data = BookingDataRequest().model_dump(mode='json')
        print(type(request_data))
        print(request_data)

        response, validated = api.booking.create(request_data)
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



    # Тут поведение системы специфическое. Ждал код 400, получил 200 с некорректными датами. Он они были обработаны
    # Оставил тест как есть. В реальном проекте уточнил бы требования
    def test_create_booking_with_invalid_dates(self, api, test_data):
        """Создание бронирования с некорректными датами"""
        request_data = test_data["booking"]["invalid_dates_post"]
        print(type(request_data))
        print(request_data)

        response, validated = api.booking.create(request_data, validate=False)
        assert_status_code(response, 400)


    # тут баг - успешное создание без поля additionalneeds (обязательное)
    @pytest.mark.parametrize("deleting_field",[
        "firstname", "lastname", "totalprice", "depositpaid", "bookingdates", "checkin", "checkout", "additionalneeds"
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





# Получение информации о бронировании:
# Получение бронирования по корректному ID
# Получение бронирования по несуществующему ID
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

# Удаление бронирования:
# Успешное удаление бронирования
# Попытка удаления без токена авторизации
# Удаление с неверным токеном авторизации
# Удаление несуществующего бронирования



