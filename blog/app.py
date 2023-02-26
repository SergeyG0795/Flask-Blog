from flask import Flask

from blog.articles.views.articles import articles_app
from blog.users.views.users import users_app


def create_app() -> Flask:
    app = Flask(__name__)
    register_blueprints(app)
    return app


def register_blueprints(app: Flask):
    app.register_blueprint(users_app, url_prefix='/users')
    app.register_blueprint(articles_app, url_prefix='/articles')
