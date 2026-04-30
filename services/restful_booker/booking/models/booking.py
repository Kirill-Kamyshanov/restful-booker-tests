import random
from datetime import date

from faker import Faker
from pydantic import BaseModel, Field

fake = Faker()

class BookingDates(BaseModel):
    """вспомогательная структура с датами заселения-выселения"""
    checkin: date
    checkout: date


class BookingDatesforPatchRequest(BaseModel):
    """вспомогательная структура с не обязательными датами заселения-выселения для PATCH запроса"""
    checkin: date | None = None
    checkout: date | None = None


class GetIdBooking(BaseModel):
    """Идентификатор брони в массиве ответа GET /booking"""
    bookingid: int = Field(gt=0)


# Просто массив объектов GetIdBooking
# GetListBookingsResponse = [GetIdBooking(**item).model_dump() for item in data]


class BookingDataRequest(BaseModel):
    """данные бронирования
    запрос POST /booking
    запрос PUT /booking/{id}
    """
    firstname: str = Field(default_factory=fake.first_name)
    lastname: str = Field(default_factory=fake.last_name)
    totalprice: int = Field(gt=0)
    depositpaid: bool = random.choice([True, False])
    bookingdates: BookingDates
    additionalneeds: str


class BookingDataResponse(BaseModel):
    """данные бронирования
    ответ GET /booking/{id}
    ответ PUT /booking/{id}
    ответ PATCH /booking/{id}
    """
    firstname: str
    lastname: str
    totalprice: int = Field(gt=0)
    depositpaid: bool
    bookingdates: BookingDates
    additionalneeds: str






class CreateBookingResponse(BaseModel):
    """ответ при успешном создании брони"""
    bookingid: int = Field(gt=0)
    booking: BookingDataResponse


class UpdateBookingPatchResponse(BaseModel):
    """запрос на частичное обновление брони"""
    firstname: str | None = None
    lastname: str | None = None
    totalprice: int | None = None
    depositpaid: bool | None = None
    bookingdates: BookingDatesforPatchRequest | None = None
    additionalneeds: str | None = None
