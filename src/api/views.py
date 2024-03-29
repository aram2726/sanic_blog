from sanic.views import HTTPMethodView

from src.infrastructure.controllers import BlogAPIController
from src.infrastructure.controllers import UserAPIController
from src.infrastructure.responses import JsonResponse
from src.infrastructure.permissions import IsAuthenticated
from src.infrastructure.permissions import IsSuperAdmin
from src.infrastructure.permissions import ViewUsersPermission
from src.infrastructure.permissions import ManageUserPermission
from src.infrastructure.permissions import ManageBlogPermission


class ListBlogPostsView(HTTPMethodView):

    async def get(self, request):
        controller = BlogAPIController(request, JsonResponse())
        await controller.list()
        return controller.response.response


class CreateBlogPostView(HTTPMethodView):

    async def post(self, request):
        controller = BlogAPIController(request, JsonResponse(), IsAuthenticated)
        await controller.create()
        return controller.response.response


class BlogPostView(HTTPMethodView):

    async def get(self, request, uuid):
        controller = BlogAPIController(request, JsonResponse())
        await controller.get(uuid)
        return controller.response.response

    async def patch(self, request, uuid):
        controller = BlogAPIController(request, JsonResponse(), ManageBlogPermission)
        await controller.update(uuid)
        return controller.response.response

    async def delete(self, request, uuid):
        controller = BlogAPIController(request, JsonResponse(), ManageBlogPermission)
        await controller.delete(uuid)
        return controller.response.response


class ListUsersView(HTTPMethodView):

    async def get(self, request):
        controller = UserAPIController(request, JsonResponse(), IsSuperAdmin)
        await controller.list()
        return controller.response.response


class CreateUserView(HTTPMethodView):

    async def post(self, request):
        controller = UserAPIController(request, JsonResponse())
        await controller.create()
        return controller.response.response


class UserView(HTTPMethodView):

    async def get(self, request, uuid):
        controller = UserAPIController(request, JsonResponse())
        await controller.get(uuid)
        return controller.response.response

    async def patch(self, request, uuid):
        controller = UserAPIController(request, JsonResponse(), ManageUserPermission)
        await controller.update(uuid)
        return controller.response.response

    async def delete(self, request, uuid):
        controller = UserAPIController(request, JsonResponse(), ManageUserPermission)
        await controller.delete(uuid)
        return controller.response.response


class LoginView(HTTPMethodView):
    async def post(self, request):
        controller = UserAPIController(request, JsonResponse())
        await controller.login()
        return controller.response.response
