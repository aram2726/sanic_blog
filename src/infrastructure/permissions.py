from abc import ABCMeta
from abc import abstractmethod
from typing import Optional

from sanic.request import Request

from .authentification import JWTManager
from .exceptions import UnauthorizedError
from src.core.entities import BlogPostEntity
from src.core.entities import UserEntity
from src.core.responses import CODE_UNAUTHORIZED


class AbstractBasePermission(metaclass=ABCMeta):

    def __init__(self, request: Request, token_manager: JWTManager):
        self.request = request
        self.token_manager = token_manager

    @abstractmethod
    def has_perm(self, *args):
        raise NotImplementedError


class IsAuthenticated(AbstractBasePermission):
    async def has_perm(self) -> Optional[UserEntity]:
        try:
            token = self.request.headers.get("Authorization")
            user = await self.token_manager.get_user(token)
            return user
        except UnauthorizedError as exc:
            return exc.args[0]


class ViewUsersPermission(AbstractBasePermission):
    def has_perm(self):
        pass


class ManageUserPermission(AbstractBasePermission):
    async def has_perm(self) -> bool:
        try:
            token = self.request.headers.get("Authorization")
            user = await self.token_manager.get_user(token)
            return user.is_superadmin if user else False
        except UnauthorizedError as exc:
            return exc.args[0]


class IsSuperAdmin(AbstractBasePermission):
    async def has_perm(self) -> bool:
        try:
            token = self.request.headers.get("Authorization")
            user = await self.token_manager.get_user(token)
            return user.is_superadmin if user else False
        except UnauthorizedError as exc:
            return exc.args[0]


class ManageBlogPermission(AbstractBasePermission):
    async def has_perm(self, blog: BlogPostEntity) -> bool:
        try:
            token = self.request.headers.get("Authorization")
            user = await self.token_manager.get_user(token)
            return blog.author == user.uuid or user.is_superadmin
        except UnauthorizedError as exc:
            return exc.args[0]
