from .config import api
from .views import ListBlogPostsView
from .views import BlogPostView
from .views import CreateBlogPostView

api.add_route(BlogPostView.as_view(), '/post/<uuid:int>')
api.add_route(ListBlogPostsView.as_view(), '/')
api.add_route(CreateBlogPostView.as_view(), '/post')
