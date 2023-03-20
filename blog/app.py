import os
from flask import Flask, render_template
from flask_login import login_manager
from flask_migrate import Migrate

from blog.models.database import db
from blog.views.articles import articles_app
from blog.views.authapp import auth_app
from blog.views.users import users_app

app = Flask(__name__)
app.register_blueprint(users_app, url_prefix='/users')
app.register_blueprint(articles_app, url_prefix='/articles')
app.register_blueprint(auth_app, url_prefix="/auth")

cfg_name = os.environ.get("CONFIG_NAME") or "ProductionConfig"
app.config.from_object(f"blog.configs.{cfg_name}")
db.init_app(app)


login_manager.init_app(app)
migrate = Migrate(app, db, compare_type=True)


@app.route("/")
def index():
    return render_template("index.html")
