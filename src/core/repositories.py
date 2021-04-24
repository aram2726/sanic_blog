from abc import ABCMeta
from abc import abstractmethod

DEFAULT_LIMIT = 10


class BaseReadOnlyRepository(metaclass=ABCMeta):

    @abstractmethod
    def get_one(self, uuid: int):
        raise NotImplementedError

    @abstractmethod
    def get_all(self, after: int = 0, limit: int = DEFAULT_LIMIT):
        raise NotImplementedError


class BaseManageableRepository(BaseReadOnlyRepository, metaclass=ABCMeta):

    @abstractmethod
    def insert(self, data: dict):
        raise NotImplementedError

    @abstractmethod
    def update(self, uuid: int, data: dict):
        raise NotImplementedError

    def delete(self, uuid: int):
        raise NotImplementedError
