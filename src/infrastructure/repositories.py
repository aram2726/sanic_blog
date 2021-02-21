from typing import List

from .databases import SQLiteDBClient
from src.core.entities import BlogPostEntity
from src.core.entities import UserEntity
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

    async def update(self, uuid: int, data: dict):
        await self.db.update(self.table, uuid, data)

    async def delete(self, uuid: int):
        await self.db.delete(self.table, uuid)


class UserRepository(BaseManageableRepository):
    def __init__(self, db: SQLiteDBClient):
        self._db = db
        self._table = "users"

    @property
    def table(self):
        return self._table

    @property
    def db(self):
        return self._db

    async def get_one(self, uuid: int) -> UserEntity:
        data = await self.db.select_one(self.table, uuid)
        return UserEntity(**data)

    async def get_all(self, after=0, limit=DEFAULT_LIMIT) -> List[UserEntity]:
        data = await self.db.select_all(self.table, limit, after)
        return [UserEntity(**item) for item in data]

    async def filter(self, data: dict):
        data = await self.db.filter(self.table, data)
        return [UserEntity(**item) for item in data]

    async def insert(self, data: dict):
        await self.db.insert(self.table, data)

    async def update(self, uuid: int, data: dict):
        await self.db.update(self.table, uuid, data)

    async def delete(self, uuid: int):
        await self.db.delete(self.table, uuid)
