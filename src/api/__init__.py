from sanic import Sanic

app = Sanic("blog")

app.config.DB_PATH = 'async_blog'

