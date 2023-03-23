from flask import Blueprint, render_template
from flask_login import login_required
from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import login_required, current_user, login_user
from werkzeug.exceptions import NotFound
from werkzeug.security import generate_password_hash

from ..extensions import db
from ..forms.user import UserRegisterForm
from ..models import User

user = Blueprint("user", __name__, url_prefix="/users", static_folder="../static")
USERS = {
    1: {"name": "Ivan"},
    2: {"name": "Jon"},
    3: {"name": "Mary"}
}


@user.route("register", methods=["POST", "GET"])
def register_user():
    if current_user.is_authenticated:
        return redirect(url_for("user.profile", pk=current_user.id))
    form = UserRegisterForm(request.form)
    errors = []
    if request.method == "POST" and form.validate_on_submit():
        if User.query.filter_by(email=form.email.data).count():
            form.email.errors.append("email not uniq")
            return render_template("users/register.html", form=form, errors=errors)
        _user = User(email=form.email.data,
                     password=generate_password_hash(form.password.data),
                     first_name=form.first_name.data,
                     last_name=form.last_name.data)
        db.session.add(_user)
        db.session.commit()

        login_user(_user)
    return render_template("users/register.html", form=form, errors=errors)


@user.route("/")
@login_required
def user_list():
    users = User.query.all()
    return render_template(
        "users/list.html",
        users=users
    )


@user.route("/<int:pk>")
@login_required
def profile(pk: int):
    _user = User.query.filter_by(id=pk).one_or_none()
    if _user is None:
        raise NotFound("User id:{}, not found".format(pk))
    return render_template(
        "users/details.html",
        user=_user
    )


def get_user_name(pk: int):
    if pk in USERS:
        user_name = USERS[pk]["name"]
    else:
        raise NotFound("User id:{}, not found".format(pk))
    return user_name
