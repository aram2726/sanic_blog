from unittest import TestCase
from src.api.routers import api


ENTITY_DATA = {
    "title": "Title",
    "context": "Context",
}


class TestAPI(TestCase):

    def setUp(self) -> None:
        self.client = ""

    def test_list_should_return_ok(self):
        request, response = api.test_client.get('/')
        assert response.status == 200

    def test_get_should_return_ok(self):
        request, response = api.test_client.get('/post/1')
        assert response.status == 200

    def test_patch_should_return_ok(self):
        request, response = api.test_client.patch('/post/1', {"title": 123})
        assert response.status == 200

    def test_post_should_return_ok(self):
        request, response = api.test_client.post('/post/1', data=ENTITY_DATA)
        assert response.status == 200

    def test_delete_should_return_ok(self):
        request, response = api.test_client.delete('/post/1')
        assert response.status == 200
