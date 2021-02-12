from abc import ABCMeta

from sanic.request import Request

from .responses import JsonResponse
from .repositories import BlogPostRepository


class BaseController(metaclass=ABCMeta):
    def __init__(self):
        self._blog_repo = None

    @property
    def blog_repo(self):
        if self._blog_repo is None:
            self._blog_repo = BlogPostRepository()
        return self._blog_repo


class BaseHttpController(BaseController):
    def __init__(self, request: Request, response: JsonResponse):
        super().__init__()
        self._request = request
        self._response = response

    @property
    def request(self):
        return self._request

    @property
    def response(self):
        return self._response


class APIController(BaseHttpController):
    def __init__(self, request: Request, response: HTTPResponse):
        super(APIController, self).__init__(request, response)

    def list(self):
        after = self.request.args.get("after")
        limit = self.request.args.get("limit")
        data = self.blog_repo.get_all(after, limit)
        self.response.data = data

    def get(self, uuid: int):
        data = self.blog_repo.get_one(uuid)
        self.response.data = data

    def create(self):
        self.blog_repo.insert(self.request.json)

    def update(self, uuid: int):
        pass

    def delete(self, uuid: int):
        pass
