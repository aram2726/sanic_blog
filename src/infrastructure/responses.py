from sanic.response import HTTPResponse as BaseHttpResponse


class JsonResponse:
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
