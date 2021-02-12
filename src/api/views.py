from sanic.views import HTTPMethodView

from src.infrastructure.controllers import APIController
from src.infrastructure.responses import JsonResponse


class ListBlogPostsView(HTTPMethodView):

    async def get(self, request):
        controller = APIController(request, JsonResponse())
        await controller.list()
        return controller.response.response


class CreateBlogPostView(HTTPMethodView):

    def post(self, request):
        controller = APIController(request, JsonResponse())
        controller.create()
        return controller.response.response


class BlogPostView(HTTPMethodView):

    def get(self, request, uuid):
        controller = APIController(request, JsonResponse())
        controller.get(uuid)
        return controller.response.response

    def patch(self, request, uuid):
        controller = APIController(request, JsonResponse())
        controller.update(uuid)
        return controller.response.response

    def delete(self, request, uuid):
        controller = APIController(request, JsonResponse())
        controller.delete(uuid)
        return controller.response.response
