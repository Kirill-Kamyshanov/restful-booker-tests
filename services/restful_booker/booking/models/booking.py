import random
from datetime import timedelta
from datetime import date

from faker import Faker
from pydantic import BaseModel, Field, field_validator

fake = Faker()

def _additional_needs():
    """Вспомогательная функция для генерации тестовых данных для поля 'additionalneeds'"""
    return random.choice(["Breakfast", "Lunch", "Dinner", "Handicapp parking", "", "Gym", "Brewery", "Пожрать"])

def _random_flag():
    """вспомогательная функция для генерации случайного значения флагов"""
    return random.choice([True, False])

def _random_price():
    """Вспомогательная функция для генерации случайного значения цены"""
    return random.randint(1000, 50000)


class BookingDates(BaseModel):
    """вспомогательная структура с датами заселения-выселения"""
    checkin: str = Field(default_factory=lambda:  (date.today() + timedelta(days=random.randrange(-30, 30))).isoformat())
    checkout: str = Field(default_factory=lambda: (date.today() + timedelta(days=random.randrange(31, 100))).isoformat())


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
    totalprice: int = Field(gt=0, default_factory=_random_price)
    depositpaid: bool = Field(default_factory=_random_flag)
    bookingdates: BookingDates = Field(default_factory=BookingDates)
    additionalneeds: str = Field(default_factory=_additional_needs)





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
