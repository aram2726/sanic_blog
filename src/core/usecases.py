from abc import ABCMeta
from abc import abstractmethod
from typing import Optional

from .repositories import BaseManageableRepository
from .responses import AbstractBaseResponse


class AbstractBaseUsecase(metaclass=ABCMeta):
    def __init__(self, response: AbstractBaseResponse, repo: BaseManageableRepository):
        self._response = response
        self._repo = repo

    @abstractmethod
    def execute(self):
        raise NotImplementedError


class ListBlogPostUsecase(AbstractBaseUsecase):

    def __init__(
            self,
            response: AbstractBaseResponse,
            repo: BaseManageableRepository,
            after: Optional[int] = None,
            limit: Optional[int] = None,
    ):
        super().__init__(response, repo)
        self._after = after
        self._limit = limit

    async def execute(self):
        self._response = self._repo.get_all(self._after, self._limit)


class GetBlogPostUsecase(AbstractBaseUsecase):

    def __init__(self, response: AbstractBaseResponse, repo: BaseManageableRepository, uuid: int):
        super().__init__(response, repo)
        self._uuid = uuid

    async def execute(self):
        pass


class UpdateBlogPostUsecase(AbstractBaseUsecase):

    def __init__(self, response: AbstractBaseResponse, repo: BaseManageableRepository, uuid: int):
        super().__init__(response, repo)
        self._uuid = uuid

    async def execute(self):
        pass


class CreateBlogPostUsecase(AbstractBaseUsecase):

    def __init__(self, response: AbstractBaseResponse, repo: BaseManageableRepository, data: dict):
        super().__init__(response, repo)
        self._data = data

    async def execute(self):
        pass


class DeleteBlogPostUsecase(AbstractBaseUsecase):

    def __init__(self, response: AbstractBaseResponse, repo: BaseManageableRepository, uuid: int):
        super().__init__(response, repo)
        self._uuid = uuid

    async def execute(self):
        pass
