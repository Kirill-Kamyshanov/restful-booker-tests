from faker import Faker

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


# возможно использовать и для booking. Если нет, вынести в тест логику (раскомментировать)
    @staticmethod
    def randomize_dynamic_fields(fields_to_update: list, test_data: dict, service: str) -> dict:
        fake = Faker()
        if service.lower() == "auth":
            random_data = {"username": fake.name(), "password": fake.password()}
            for field in test_data:
                if field in fields_to_update:
                    test_data[field] = random_data[field]
            return test_data
        return {}