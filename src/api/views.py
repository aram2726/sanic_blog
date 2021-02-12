from sanic.views import HTTPMethodView

from src.infrastructure.controllers import APIController
from src.infrastructure.responses import JsonResponse


class ListBlogPostsView(HTTPMethodView):

    async def get(self, request):
        controller = APIController(request, JsonResponse())
        await controller.list()
        return controller.response.response


class CreateBlogPostView(HTTPMethodView):

    async def post(self, request):
        controller = APIController(request, JsonResponse())
        await controller.create()
        return controller.response.response


class BlogPostView(HTTPMethodView):

    async def get(self, request, uuid):
        controller = APIController(request, JsonResponse())
        await controller.get(uuid)
        return controller.response.response

    async def patch(self, request, uuid):
        controller = APIController(request, JsonResponse())
        await controller.update(uuid)
        return controller.response.response

    async def delete(self, request, uuid):
        controller = APIController(request, JsonResponse())
        await controller.delete(uuid)
        return controller.response.response
