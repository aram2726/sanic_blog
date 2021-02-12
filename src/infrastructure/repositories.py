from typing import List

from src.core.entities import BlogPostEntity
from src.core.repositories import BaseManageableRepository
from src.core.repositories import DEFAULT_LIMIT


class BlogPostRepository(BaseManageableRepository):

    def get_one(self, uuid: int) -> BlogPostEntity:
        pass

    def get_all(self, after=0, limit=DEFAULT_LIMIT) -> List[BlogPostEntity]:
        pass

    def insert(self, data: dict):
        pass

    def update(self, uuid: int, data: dict):
        pass

    def delete(self, uuid: int):
        pass
