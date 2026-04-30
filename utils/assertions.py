from requests import Response

def assert_status_code(response: Response, expected_code: int) -> None:
    """Проверка, что полученный статус-код соответствует ожидаемому"""
    assert response.status_code == expected_code, \
        f"Ожидался статус-код {expected_code}, но получен {response.status_code} : {response.text}"