from typing import Literal

from requests import Response

from services.base_api import BaseAPI
from services.restful_booker.booking.models.booking import (
    BookingData,
    CreateBookingResponse,
    GetIdBooking,
    UpdateBookingPatchRequest,
)


class BookingClient(BaseAPI):
    """Фасад над ресурсом /booking"""

    def create(self, request_body: str, validate: bool = True) -> tuple[Response, CreateBookingResponse | None]:
        """POST /booking — создаёт бронь и возвращает валидированный ответ"""
        response = self.post("/booking", json=request_body)
        body = CreateBookingResponse(**response.json()) if validate else None
        return response, body

    def remove(self, booking_id: int, **kwargs) -> tuple[Response, str]:
        """DELETE /booking/{id} — удаляет бронь и возвращает текст"""
        response = self.delete(f"/booking/{booking_id}", **kwargs)
        return response, response.text

    def get_by_id(self, booking_id: int, validate: bool = True) -> tuple[Response, BookingData | str]:
        """GET /booking/{id} — получение бронирования по id, возвращает JSON/текст"""
        response = self.get(f"/booking/{booking_id}")
        body = BookingData(**response.json()) if validate else response.text
        return response, body

    def get_list_bookings(self, params: dict | None = None) -> tuple[Response, list[GetIdBooking]]:
        """GET /booking — получение списка бронирований, возвращение ответа и валидированного JSON"""
        response = self.get("/booking", params=params)
        validated = [GetIdBooking(**item).model_dump() for item in response.json()]
        return response, validated

    def update_booking(self, booking_id: str | int, validated: BookingData | UpdateBookingPatchRequest,
                       method: Literal["put", "patch"], validate: bool = True, **kwargs) \
            -> tuple[Response, BookingData | str]:
        """PUT/PATCH /booking/{id} — полное/частичное обновление бронирования, возвращение JSON/текст"""
        if method.lower() == "put":
            response = self.put(f"/booking/{booking_id}", json=validated, **kwargs)
        elif method.lower() == "patch":
            response = self.patch(f"/booking/{booking_id}", json=validated, **kwargs)
        body = BookingData(**response.json()) if validate else response.text
        return response, body
