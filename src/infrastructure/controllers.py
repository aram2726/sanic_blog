from abc import ABCMeta

from sanic.request import Request

import permissions
from .authentification import JWTManager
from .config import SECRET_KEY
from .config import SQLITE_FILE_PATH
from .databases import SQLiteDBClient
from .migrations import Migration
from .responses import JsonResponse
from .repositories import BlogPostRepository
from .repositories import UserRepository
from .validators import UserValidator
from .validators import LoginValidator
from src.core import usecases
from src.core.responses import CODE_DELETED
from src.core.responses import CODE_CREATED
from src.core.entities import BlogPostEntity
from src.core.entities import UserEntity


class AbstractBaseController(metaclass=ABCMeta):
    def __init__(self):
        self._blog_repo = None
        self._user_repo = None
        self._db = None

    @property
    def db(self) -> SQLiteDBClient:
        if not self._db:
            self._db = SQLiteDBClient(SQLITE_FILE_PATH)JWTManager
        return self._db

    @property
    def blog_repo(self) -> BlogPostRepository:
        if self._blog_repo is None:
            self._blog_repo = BlogPostRepository(self.db)
        return self._blog_repo

    @property
    def user_repo(self) -> UserRepository:
        if self._user_repo is None:
            self._user_repo = UserRepository(self.db)
        return self._user_repo


class BaseHttpController(AbstractBaseController):
    data_validator_cls = None
    permission_cls = None

    def __init__(self, request: Request, output: JsonResponse):
        super().__init__()
        self._request = request
        self._response = output

        if self.permission_cls:
            self.permission_cls(request)

    @property
    def request(self):
        return self._request

    @property
    def response(self):
        return self._response


class BlogAPIController(BaseHttpController):
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
        post = BlogPostEntity(**self.request.json)
        usecase = usecases.CreateBlogPostUsecase(
            self.response, self.blog_repo, post)
        await usecase.execute()

    async def update(self, uuid: int):
        usecase = usecases.UpdateBlogPostUsecase(self.response, self.blog_repo, uuid)
        await usecase.execute()

    async def delete(self, uuid: int):
        usecase = usecases.DeleteBlogPostUsecase(self.response, self.blog_repo, uuid)
        await usecase.execute()
        self.response.status = CODE_DELETED


class UserAPIController(BaseHttpController):
    permission_class = None

    async def login(self):
        self.data_validator_cls = LoginValidator
        data = self.request.json
        validator = self.data_validator_cls(**data)
        validator.validate()

        users = await self.user_repo.filter(data)
        if users:
            token_manager = JWTManager(self.request, SECRET_KEY)
            user = users[0]



    async def list(self):
        self.permission_cls = permissions.IsSuperAdmin
        after = self.request.args.get("after")
        limit = self.request.args.get("limit")
        usecase = usecases.ListUserUsecase(self.response, self.user_repo, after, limit)
        await usecase.execute()

    async def get(self, uuid: int):
        usecase = usecases.GetUserUsecase(self.response, self.user_repo, uuid)
        await usecase.execute()

    async def create(self):
        self.data_validator_cls = UserValidator
        data = self.request.json
        validator = self.data_validator_cls(**data)
        validator.validate()

        password = data.pop("password")
        user = UserEntity(**data)
        user.password = password
        usecase = usecases.CreateUserUsecase(
            self.response, self.user_repo, user)
        await usecase.execute()
        self.response.status = CODE_CREATED

    async def update(self, uuid: int):
        self.data_validator_cls = UserValidator
        data = self.request.json
        validator = self.data_validator_cls(**data)
        validator.validate()

        password = data.pop("password")
        user = UserEntity(**data)
        user.password = password

        usecase = usecases.UpdateUserUsecase(self.response, self.user_repo, uuid, user)
        await usecase.execute()

    async def delete(self, uuid: int):
        usecase = usecases.DeleteUserUsecase(self.response, self.user_repo, uuid)
        await usecase.execute()
        self.response.status = CODE_DELETED


class CLIController(AbstractBaseController):

    def migrate(self):
        migration = Migration(self.db)
        migration.create_blog_table()
        migration.create_users_table()

    async def create_superuser(self, username: str, email: str, password: str):
        user = UserEntity(username=username, email=email)
        user.password = password
        user.is_superadmin = True
        await self.user_repo.insert(user.serialize())
