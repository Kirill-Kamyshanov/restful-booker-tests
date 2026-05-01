
from requests import Response

from services.base_api import BaseAPI
from services.restful_booker.booking.models.booking import CreateBookingResponse, BookingDataResponse, GetIdBooking, \
    BookingDataRequest


class BookingClient(BaseAPI):
    """Фасад над ресурсом /booking"""

    def create(self, request_body: str, validate: bool = True) -> tuple[Response, CreateBookingResponse | None]:
        """POST /booking — создаёт бронь и возвращает валидированный ответ"""
        response = self.post("/booking",json=request_body)
        body = CreateBookingResponse(**response.json())  if validate else None
        return response, body


    def remove(self, booking_id: int, **kwargs) -> tuple[Response, str]:
        """DELETE /booking/{id} — удаляет бронь и возвращает текст"""
        response = self.delete(f"/booking/{booking_id}", **kwargs)
        return response, response.text


    def get_by_id(self, booking_id: int, validate: bool = True) -> tuple[Response, BookingDataResponse | str]:
        """GET /booking/{id} — получение бронирования по id, возвращение JSON"""
        response = self.get(f"/booking/{booking_id}")
        body = BookingDataResponse(**response.json()) if validate else response.text
        return response, body


    def get_list_bookings(self, params: dict|None = None) -> tuple[Response, list[GetIdBooking]]:
        """GET /booking — получение списка бронирований, возвращение JSON"""
        response = self.get(f"/booking", params=params)
        validated = [GetIdBooking(**item).model_dump() for item in response.json()]
        # print(body)
        return response, validated


    def put_update_booking(self, booking_id: str|int, validated: BookingDataRequest) \
            -> tuple[Response, BookingDataResponse]:
        """PUT /booking/{id} — полное обновление бронирования, возвращение JSON"""
        response = self.put(f"/booking/{booking_id}", json=validated)
        return response, BookingDataResponse(**response.json())