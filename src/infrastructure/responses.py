import json

from sanic.response import HTTPResponse as BaseHttpResponse

from .encoders import ResponseEncoder
from src.core.responses import AbstractBaseResponse


class JsonResponse(AbstractBaseResponse):
    def __init__(self):
        self._response = BaseHttpResponse()
        self._response.content_type = "application/json"

    @property
    def status(self):
        return self._response.status

    @status.setter
    def status(self, status: str):
        self._response.status = status

    @property
    def response(self):
        return self._response

    @property
    def data(self):
        return self._response.body

    @data.setter
    def data(self, data: dict):
        self._response.body = bytes(json.dumps(data, cls=ResponseEncoder), encoding="UTF-8")

    @property
    def headers(self):
        return self._response.get_headers()
