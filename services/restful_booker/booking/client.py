
from requests import Response

from services.base_api import BaseAPI
from services.restful_booker.booking.models.booking import CreateBookingResponse


class BookingClient(BaseAPI):
    """Фасад над ресурсом /booking"""

    def create(self, request_body, validate: bool = True) -> tuple[Response, CreateBookingResponse | None]:
        """POST /booking — создаёт бронь и возвращает валидированный ответ"""
        response = self.post("/booking",json=request_body)
        if validate:
            return response, CreateBookingResponse(**response.json())
        else:
            return response, None

    def remove(self, booking_id, **kwargs) -> tuple[Response, str]:
        """DELETE /booking/{id} — удаляет бронь и возвращает текст"""
        response = self.delete(f"/booking/{booking_id}", **kwargs)
        print(response)
        print(response.text)
        return response, response.text