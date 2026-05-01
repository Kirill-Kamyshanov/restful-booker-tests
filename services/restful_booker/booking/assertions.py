from requests import Response

from services.restful_booker.booking.models.booking import CreateBookingResponse, BookingDataRequest, \
    BookingDataResponse
from utils.assertions import assert_status_code, assert_text


def assert_creation(response: Response,
                    validated: CreateBookingResponse,
                    expected_firstname: str,
                    expected_lastname: str,
                    expected_totalprice: int,
                    expected_depositpaid: bool,
                    expected_bookingdates: dict,
                    expected_additionalneeds: str) -> None:
    """Проверка создания бронирования"""
    print(validated)
    print(type(validated))
    # print(validated.booking)
    assert_status_code(response, 200)
    assert validated.bookingid, f"Отсутствует поле bookingid"
    assert validated.booking.firstname == expected_firstname, f"Ожидалось firstname={expected_firstname}, но получено {validated.booking.firstname}"
    assert validated.booking.lastname == expected_lastname, f"Ожидалось lastname={expected_lastname}, но получено {validated.booking.lastname}"
    assert validated.booking.totalprice == expected_totalprice, f"Ожидалось totalprice={expected_totalprice}, но получено {validated.booking.totalprice}"
    assert validated.booking.depositpaid == expected_depositpaid, f"Ожидалось depositpaid={expected_depositpaid}, но получено {validated.booking.depositpaid}"
    assert validated.booking.bookingdates.checkin == expected_bookingdates["checkin"], f"Ожидалось checkin={expected_bookingdates["checkin"]}, но получено {validated.booking.bookingdates.checkin}"
    assert validated.booking.bookingdates.checkout == expected_bookingdates["checkout"], f"Ожидалось checkout={expected_bookingdates["checkout"]}, но получено {validated.booking.bookingdates.checkout}"
    assert validated.booking.additionalneeds == expected_additionalneeds, f"Ожидалось additionalneeds={expected_additionalneeds}, но получено {validated.booking.additionalneeds}"




def assert_code_and_text(response: Response, expected_code: int, expected_text :str) -> None:
    """Проверка статус-кода и текста ответа"""
    assert_status_code(response, expected_code)
    assert_text(response, expected_text)


def assert_get_by_id(response: Response, response_body: BookingDataResponse) -> None:
    """Проверка получения данных бронирования по id"""
    assert_status_code(response, 200)
