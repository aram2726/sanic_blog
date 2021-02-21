from .config import api
from .views import ListBlogPostsView
from .views import BlogPostView
from .views import CreateBlogPostView
from .views import ListUsersView
from .views import CreateUserView
from .views import UserView

api.add_route(BlogPostView.as_view(), '/post/<uuid:int>')
api.add_route(ListBlogPostsView.as_view(), '/posts')
api.add_route(CreateBlogPostView.as_view(), '/post/')

api.add_route(UserView.as_view(), '/user/<uuid:int>')
api.add_route(ListUsersView.as_view(), '/users')
api.add_route(CreateUserView.as_view(), '/user/')
