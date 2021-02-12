from typing import List

from .databases import SQLiteDBClient
from src.core.entities import BlogPostEntity
from src.core.repositories import BaseManageableRepository
from src.core.repositories import DEFAULT_LIMIT


class BlogPostRepository(BaseManageableRepository):

    def __init__(self, db: SQLiteDBClient):
        self._db = db
        self._table = "blog"

    @property
    def table(self):
        return self._table

    @property
    def db(self):
        return self._db

    async def get_one(self, uuid: int) -> BlogPostEntity:
        data = await self.db.select_one(self.table, uuid)
        return BlogPostEntity(**data)

    async def get_all(self, after=0, limit=DEFAULT_LIMIT) -> List[BlogPostEntity]:
        data = await self.db.select_all(self.table, limit, after)
        return [BlogPostEntity(**item) for item in data]

    async def insert(self, data: dict):
        await self.db.insert(self.table, data)

    def update(self, uuid: int, data: dict):
        pass

    def delete(self, uuid: int):
        pass
