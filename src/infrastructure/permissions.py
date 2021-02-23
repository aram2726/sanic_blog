from abc import ABCMeta
from abc import abstractmethod

from sanic.request import Request

from .exceptions import UnauthorizedError
from .exceptions import PermissionDeniedError


class AbstractBasePermission(metaclass=ABCMeta):

    def __init__(self, request: Request):
        self.request = request

    @abstractmethod
    def has_perm(self):
        raise NotImplementedError


class IsAuthenticated(AbstractBasePermission):
    def has_perm(self):
        pass


class ViewUsersPermission(AbstractBasePermission):
    def has_perm(self):
        pass


class ManageUserPermission(AbstractBasePermission):
    def has_perm(self):
        pass


class IsSuperAdmin(AbstractBasePermission):
    def has_perm(self):
        pass


class ManageBlogPermission(AbstractBasePermission):
    def has_perm(self):
        pass
