from services.base_api import BaseAPI
from requests import Response

from services.restful_booker.auth.models.auth import AuthResponse, AuthErrorResponse


class AuthClient(BaseAPI):
    """Фасад над ресурсом /auth"""

    def login(self, request_body: str, is_positive: bool = True) -> tuple[Response, AuthResponse | AuthErrorResponse]:
        """Отправка запроса на авторизацию"""
        response = self.post("/auth", json=request_body)
        if is_positive:
            return response, AuthResponse(**response.json())
        else:
            return response, AuthErrorResponse(**response.json())


