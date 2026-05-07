from requests import Response

from services.base_api import BaseAPI
from services.restful_booker.auth.models.auth import AuthErrorResponse, AuthResponse


class AuthClient(BaseAPI):
    """Фасад над ресурсом /auth"""

    def login(self, request_body: dict, validate: bool = True) -> tuple[Response, AuthResponse | AuthErrorResponse]:
        """POST /auth - Отправка запроса на авторизацию"""
        response = self.post("/auth", json=request_body)
        body = AuthResponse(**response.json()) if validate else AuthErrorResponse(**response.json())
        return response, body
