from unittest import TestCase
from unittest.mock import Mock

from src.infrastructure.databases import SQLiteDBClient
from src.core.entities import BlogPostEntity
from src.core.entities import UserEntity

user = UserEntity(**{
    "uuid": 1,
    "username": "user",
    "email": "user@example.com",
    "password": "string123",
})

blog = BlogPostEntity(**{
    "title": "Title",
    "context": "Context",
    "author": user
})


class TestSQLiteDBClient(TestCase):

    def setUp(self):
        self.client = SQLiteDBClient(":memory:")
        self.client.cursor = Mock()

    async def test_select_one(self):
        self.client.cursor.return_value.fetcone.return_value = blog
        item = await self.client.select_one("blog", 1)
        assert isinstance(item, BlogPostEntity)

    async def test_select_all(self):
        self.client.cursor.return_value.fetchall.return_value = [blog]
        items = await self.client.select_all("blog")

        assert len(items) == 1
        assert isinstance(items[0], BlogPostEntity)
