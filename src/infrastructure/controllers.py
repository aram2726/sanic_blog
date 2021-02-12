from abc import ABCMeta

from sanic.request import Request

from .config import SQLITE_FILE_PATH
from .databases import SQLiteDBClient
from .migrations import Migration
from .responses import JsonResponse
from .repositories import BlogPostRepository
from src.core import usecases


class AbstractBaseController(metaclass=ABCMeta):
    def __init__(self):
        self._blog_repo = None
        self._db = None

    @property
    def db(self) -> SQLiteDBClient:
        if not self._db:
            self._db = SQLiteDBClient(SQLITE_FILE_PATH)
        return self._db

    @property
    def blog_repo(self) -> BlogPostRepository:
        if self._blog_repo is None:
            self._blog_repo = BlogPostRepository(self.db)
        return self._blog_repo


class BaseHttpController(AbstractBaseController):
    def __init__(self, request: Request, output: JsonResponse):
        super().__init__()
        self._request = request
        self._response = output

    @property
    def request(self):
        return self._request

    @property
    def response(self):
        return self._response


class APIController(BaseHttpController):
    def __init__(self, request: Request, response: JsonResponse):
        super().__init__(request, response)

    async def list(self):
        after = self.request.args.get("after")
        limit = self.request.args.get("limit")
        usecase = usecases.ListBlogPostUsecase(self.response, self.blog_repo, after, limit)
        await usecase.execute()

    async def get(self, uuid: int):
        usecase = usecases.GetBlogPostUsecase(self.response, self.blog_repo, uuid)
        await usecase.execute()

    async def create(self):
        usecase = usecases.CreateBlogPostUsecase(
            self.response, self.blog_repo, self.request.json)
        await usecase.execute()

    async def update(self, uuid: int):
        usecase = usecases.UpdateBlogPostUsecase(self.response, self.blog_repo, uuid)
        await usecase.execute()

    async def delete(self, uuid: int):
        usecase = usecases.DeleteBlogPostUsecase(self.response, self.blog_repo, uuid)
        await usecase.execute()


class CLIController(AbstractBaseController):

    def migrate(self):
        migration = Migration(self.db)
        migration.create_table()
