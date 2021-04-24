import asyncio
from unittest import TestCase
from src.api.routers import api

from src.core.entities import UserEntity

USER_ENTITY_DATA = {
    "uuid": 1,
    "username": "user",
    "email": "user@example.com",
    "password": "string123",
}

BLOG_ENTITY_DATA = {
    "title": "Title",
    "context": "Context",
    "author": UserEntity(**USER_ENTITY_DATA)
}


class TestBlogAPI(TestCase):

    async def test_blog_list_should_return_ok(self):
        request, response = await api.test_client.get('/posts')
        assert response.status == 200

    async def test_blog_get_should_return_ok(self):
        request, response = await api.test_client.get('/post/1')
        assert response.status == 200

    async def test_blog_patch_should_return_ok(self):
        request, response = await api.test_client.patch('/post/1', {"title": 123})
        assert response.status == 200

    async def test_blog_post_should_return_ok(self):
        request, response = await api.test_client.post('/post/1', data=BLOG_ENTITY_DATA)
        assert response.status == 200

    async def test_blog_delete_should_return_ok(self):
        request, response = await api.test_client.delete('/post/1')
        assert response.status == 200


class TestUserAPI(TestCase):

    async def test_users_list_should_return_ok(self):
        request, response = await api.test_client.get('/users')
        assert response.status == 200

    async def test_get_should_return_ok(self):
        request, response = await api.test_client.get('/user/1')
        assert response.status == 200

    async def test_users_patch_should_return_ok(self):
        request, response = await api.test_client.patch('/users/1', {"username": "john"})
        assert response.status == 200

    async def test_users_post_should_return_ok(self):
        request, response = await api.test_client.post('/user/', data=USER_ENTITY_DATA)
        assert response.status == 200

    async def test_users_delete_should_return_ok(self):
        request, response = await api.test_client.delete('/user/1')
        assert response.status == 200
