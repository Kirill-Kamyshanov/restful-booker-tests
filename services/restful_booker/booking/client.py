
from requests import Response

from services.base_api import BaseAPI
from services.restful_booker.booking.models.booking import CreateBookingResponse, BookingDataResponse


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
