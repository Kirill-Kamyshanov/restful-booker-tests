from requests import Response

from services.restful_booker.booking.models.booking import BookingData, CreateBookingResponse, UpdateBookingPatchRequest
from utils.assertions import assert_response_text, assert_status_code


def assert_booking_created(response: Response, request_body: dict, response_body: CreateBookingResponse) -> None:
    """Проверка создания бронирования"""
    assert_status_code(response, 200)
    assert request_body == response_body.booking.model_dump(), "Тело ответа отличается от тела запроса"


def assert_code_and_text(response: Response, expected_code: int, expected_text: str) -> None:
    """Проверка статус-кода и текста ответа"""
    assert_status_code(response, expected_code)
    assert_response_text(response, expected_text)


def assert_get_by_id(response: Response, response_body: BookingData) -> None:
    """Проверка получения данных бронирования по id. Пока метод проверяет только код,
    т.к. нет особой логики в теле ответа"""
    assert_status_code(response, 200)


def assert_booking_updated_put(response: Response, new_data: BookingData, actual_data: BookingData) -> None:
    """Проверка полного обновления бронирования"""
    assert_status_code(response, 200)
    assert new_data == actual_data, "Данные в ответе не совпадают с переданными в PUT-запросе"


def assert_booking_updated_patch(response: Response, new_data: UpdateBookingPatchRequest, actual_data: BookingData)\
        -> None:
    """Проверка частичного обновления бронирования.
    В текущей реализации проверяет только плоские поля на верхнем уровне"""
    assert_status_code(response, 200)
    actual_dict = actual_data.model_dump()
    for k, v in new_data.items():
        assert actual_dict[k] == v, f"Ожидалось значение {k} == {v}, но получено {actual_dict[k]}"
