from abc import ABCMeta
from abc import abstractmethod

from sanic.request import Request

from .exceptions import UnauthorizedError
from .exceptions import PermissionDeniedError


class AbstractBasePermission(metaclass=ABCMeta):

    @abstractmethod
    def has_perm(self, request: Request):
        raise NotImplementedError


class IsAuthenticated(AbstractBasePermission):
    def has_perm(self, request: Request):
        pass


class ViewUsersPermission(AbstractBasePermission):
    def has_perm(self, request: Request):
        pass


class ManageUserPermission(AbstractBasePermission):
    def has_perm(self, request: Request):
        pass


class IsSuperAdmin(AbstractBasePermission):
    def has_perm(self, request: Request):
        pass


class ManageBlogPermission(AbstractBasePermission):
    def has_perm(self, request: Request):
        pass
