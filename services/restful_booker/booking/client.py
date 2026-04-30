from requests import Response

from services.base_api import BaseAPI


class BookingClient(BaseAPI):
    """Фасад над ресурсом /booking"""

    def create_booking(self) -> tuple[Response, ]:
        pass