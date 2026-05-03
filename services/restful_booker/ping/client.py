from requests import Response

from services.base_api import BaseAPI


class PingClient(BaseAPI):
    """Фасад над ресурсом /ping"""

    def ping(self) -> tuple[Response, str]:
        """GET /ping - проверка работоспособности API"""
        response = self.get('/ping')
        return response, response.text
