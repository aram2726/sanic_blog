from sanic.response import HTTPResponse as BaseHttpResponse

from src.core.responses import AbstractBaseResponse


class JsonResponse(AbstractBaseResponse):
    def __init__(self):
        self._response = BaseHttpResponse()
        self._response.content_type = "application/json"

    @property
    def response(self):
        return self._response

    @property
    def data(self):
        return self._response.body

    @data.setter
    def data(self, data: dict):
        self._response.body = data

    @property
    def headers(self):
        return self._response.get_headers()
