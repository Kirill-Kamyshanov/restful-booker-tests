import logging
from typing import Any
import json as json_lib

import allure
from requests import Response

logger = logging.getLogger("api")

DEFAULT_TIMEOUT = 30
DEFAULT_RETRIES = 3
DEFAULT_BACKOFF = 0.3
RETRY_STATUSES = (500, 502, 503, 504)



class BaseAPI:
    """Базовый HTTP-клиент: единый _request с retry, structured-logging и request_id"""

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
















    # @staticmethod
    # def _attach_response(response: Response, elapsed_ms: float, request_id: str) -> None:
    #     """Прикрепляет к Allure тело ответа c request_id, статусом и длительностью; не-JSON отдаёт как текст."""
    #     try:
    #         payload = json_lib.dumps(response.json(), indent=2, ensure_ascii=False)
    #         atype = allure.attachment_type.JSON
    #     except (ValueError, json_lib.JSONDecodeError):
    #         payload = response.text or f"<empty body, status {response.status_code}>"
    #         atype = allure.attachment_type.TEXT
    #     body = f"# request_id={request_id} status={response.status_code} elapsed_ms={elapsed_ms:.0f}\n{payload}"
    #     allure.attach(body=body, name=f"RESPONSE {response.status_code}", attachment_type=atype)