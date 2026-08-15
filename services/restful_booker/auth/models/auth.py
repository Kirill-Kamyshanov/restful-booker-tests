from pydantic import BaseModel


class AuthRequest(BaseModel):
    """Запрос на создание авторизационного токена"""

    username: str
    password: str


class AuthResponse(BaseModel):
    """Успешный ответ при авторизации"""

    token: str


class AuthErrorResponse(BaseModel):
    """Ответ при ошибке авторизации"""

    reason: str
