import logging
from typing import Any
import json as json_lib

import allure
from requests import Response, Session
from requests.adapters import HTTPAdapter
from urllib3 import Retry

logger = logging.getLogger("api")

DEFAULT_TIMEOUT = 30
DEFAULT_RETRIES = 3
DEFAULT_BACKOFF = 0.3
RETRY_STATUSES = (500, 502, 503, 504)



class BaseAPI:
    """Базовый HTTP-клиент: единый _request с retry, structured-logging и request_id"""

    def __init__(self, env_config, timeout: int = DEFAULT_TIMEOUT) -> None:
        """Инициализирует клиент с базовым URL, таймаутом и преднастроенной requests.Session."""
        self.base_url = env_config.booking_url.rstrip("/")
        self.timeout = timeout
        self.session = self._build_session(env_config)




    @staticmethod
    def _build_session(env_config) -> Session:
        """Создаёт requests.Session с retry-политикой для 5xx, пулом соединений и дефолтными заголовками."""
        session = Session()
        retry = Retry(
            total=DEFAULT_RETRIES,
            backoff_factor=DEFAULT_BACKOFF,
            status_forcelist=RETRY_STATUSES,
            allowed_methods=("HEAD", "GET", "OPTIONS", "PUT", "DELETE"),
            raise_on_status=False,
            respect_retry_after_header=True,
        )
        adapter = HTTPAdapter(max_retries=retry, pool_connections=20, pool_maxsize=20)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        session.headers.update({"Content-Type": "application/json", "Accept": "application/json"})
        if getattr(env_config, "authorization", ""):
            session.headers["authorization"] = env_config.authorization
        return session




    @staticmethod
    def _attach_request(
            method: str,
            url: str,
            headers: Any,
            body: Any,
            params: Any,
            request_id: str
    ) -> None:
        data = {
            'method': method,
            'url': url,
            'headers': dict(headers),
            'body': body,
            'params': params,
            'request_id': request_id
        }
        allure.attach(
            body=json_lib.dumps(data, indent=2, ensure_ascii=False, default=str),
            name=f"REQUEST {method} {url}",
            attachment_type=allure.attachment_type.JSON,
        )



    @staticmethod
    def _attach_response(response: Response, elapsed_ms: float, request_id: str) -> None:
        """Прикрепляет к Allure тело ответа c request_id, статусом и длительностью; не-JSON отдаёт как текст."""
        try:
            payload = json_lib.dumps(response.json(), indent=2, ensure_ascii=False, default=str)
            atype = allure.attachment_type.JSON
        except (ValueError, json_lib.JSONDecodeError):
            payload = response.text or f"<empty body, status {response.status_code}>"
            atype = allure.attachment_type.TEXT
        body = f"# request_id={request_id} status={response.status_code} elapsed_ms={elapsed_ms:.0f}\n{payload}"
        allure.attach(body=body, name=f"RESPONSE {response.status_code}", attachment_type=atype)








