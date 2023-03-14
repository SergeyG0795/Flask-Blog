from flask import Flask, render_template
from flask_login import login_manager

from blog.models.database import db
from blog.views.articles import articles_app
from blog.views.authapp import auth_app
from blog.views.users import users_app

app = Flask(__name__)
app.register_blueprint(users_app, url_prefix='/users')
app.register_blueprint(articles_app, url_prefix='/articles')
app.register_blueprint(auth_app, url_prefix="/auth")

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

app.config["SECRET_KEY"] = "abcdefg123456"


login_manager.init_app(app)


@app.route("/")
def index():
    return render_template("index.html")
