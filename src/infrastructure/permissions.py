from abc import ABCMeta
from abc import abstractmethod
from typing import Optional

from sanic.request import Request

from .authentification import JWTManager
from src.core.entities import BlogPostEntity
from src.core.entities import UserEntity


class AbstractBasePermission(metaclass=ABCMeta):

    def __init__(self, request: Request, token_manager: JWTManager):
        self.request = request
        self.token_manager = token_manager

    @abstractmethod
    def has_perm(self, *args):
        raise NotImplementedError


class IsAuthenticated(AbstractBasePermission):
    async def has_perm(self) -> Optional[UserEntity]:
        token = self.request.headers.get("Authorization")
        user = await self.token_manager.get_user(token)
        return user


class ViewUsersPermission(AbstractBasePermission):
    def has_perm(self):
        pass


class ManageUserPermission(AbstractBasePermission):
    async def has_perm(self) -> bool:
        token = self.request.headers.get("Authorization")
        user = await self.token_manager.get_user(token)
        return user.is_superadmin if user else False


class IsSuperAdmin(AbstractBasePermission):
    async def has_perm(self) -> bool:
        token = self.request.headers.get("Authorization")
        user = await self.token_manager.get_user(token)
        return user.is_superadmin if user else False


class ManageBlogPermission(AbstractBasePermission):
    async def has_perm(self, blog: BlogPostEntity) -> bool:
        token = self.request.headers.get("Authorization")
        user = await self.token_manager.get_user(token)
        return blog.author == user.uuid or user.is_superadmin
