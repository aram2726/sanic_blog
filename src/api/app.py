from sanic.views import HTTPMethodView

from src.api import app
from src.infrastructure.controllers import APIController
from src.infrastructure.responses import JsonResponse


class ListBlogPostsView(HTTPMethodView):

    def get(self, request):
        controller = APIController(request, JsonResponse())
        controller.list()


class GetBlogPostView(HTTPMethodView):

    def get(self, request, uuid):
        controller = APIController(request, JsonResponse())
        controller.get(uuid)


class CreateBlogPostView(HTTPMethodView):

    def post(self, request):
        controller = APIController(request, JsonResponse())


class UpdateBlogPostView(HTTPMethodView):

    def patch(self, request):
        controller = APIController(request, JsonResponse())


app.add_route(ListBlogPostsView.as_view(), '/')
app.add_route(GetBlogPostView.as_view(), '/post/<id:int>')
app.add_route(UpdateBlogPostView.as_view(), '/post/<id:int>')
app.add_route(CreateBlogPostView.as_view(), '/post')

