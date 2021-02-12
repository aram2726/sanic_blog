from abc import ABCMeta
from abc import abstractmethod

from .repositories import BaseManageableRepository


class BaseUsecase(metaclass=ABCMeta):
    def __init__(self, repo: BaseManageableRepository):
        self._repo = repo

    @abstractmethod
    def execute(self):
        raise NotImplementedError
