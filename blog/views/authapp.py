from flask import Blueprint, redirect, url_for, request, render_template, flash
from flask_login import LoginManager, login_user, login_required, logout_user
from werkzeug.security import check_password_hash

from ..forms.auth import AuthForm
from blog.models import User

auth_app = Blueprint('auth_app', __name__)

login_manager = LoginManager()
login_manager.login_view = 'auth_app.login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=user_id).one_or_none()


@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for('auth_app.login'))


@auth_app.route('/login/', methods=['GET', 'POST'], endpoint='login')
def login():
    form = AuthForm(request.form)
    errors = []
    if request.method == "GET":
        if current_user.is_authenticated:
            return redirect(url_for("user.profile", pk=current_user.id))
        return render_template(
            "auth/login.html"
        )

        return render_template("auth/login.html", form=form, errors=errors)

    email = request.form.get("email")
    password = request.form.get("password")
    user = User.query.filter_by(email=email).first()
    if request.method == "POST":
        if form.register.data:
            return redirect(url_for("user.register_user"))

        if form.submit.data:
            email = form.email.data
            password = form.password.data
            user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password, password):
        flash("Check your login details")
        return redirect(url_for(".login"))
    login_user(user)
    return redirect(url_for("user.profile", pk=user.id))
    if not user or not check_password_hash(user.password, password):
        # Не понял почему-то password и email имеют errors типом "tuple", пришлось пере присваивать "list"
        form.password.errors = ["Check your login details"]
        return render_template(
            "auth/login.html", form=form, errors=errors
        )
    login_user(user)
    return redirect(url_for("user.profile", pk=user.id))


@auth_app.route("/logout/", endpoint="logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))


@auth_app.route("/secret/")
@login_required
def secret_view():
    return 'Super secret data'


__all__ = [
    'login_manager',
    'auth_app',
]
