import requests
from .exceptions import (
    BadRequestError,
    InternalServerError,
    InvalidApiKeyError,
    TwelveDataError,
)


class HttpClient:
    def __init__(self, base_url):
        self.base_url = base_url

    def get(self, relative_url, **params):
        url = self.base_url + relative_url
        resp = requests.get(url, timeout=10, **params)

        if not resp.ok:
            self._raise_error(resp.status_code, resp.text)

        json_resp = resp.json()
        if "status" not in json_resp:
            return resp

        status = json_resp["status"]
        if status == "error":
            error_code = json_resp["code"]
        else:
            return resp

        try:
            message = json_resp["message"]
        except ValueError:
            message = resp.text

        self._raise_error(error_code, message)

    @staticmethod
    def _raise_error(error_code, message):
        if error_code == 401:
            raise InvalidApiKeyError(message)

        if error_code == 400:
            raise BadRequestError(message)

        if error_code >= 500:
            raise InternalServerError(message)

        raise TwelveDataError(message)
