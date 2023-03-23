import click
from werkzeug.security import generate_password_hash

from .extensions import db


@click.command("init-db", help="create all db")
def init_db():
    from wsgi import app
    with app.app_context():
        db.create_all()


@click.command("create-users", help="create users")
def create_users():
    from .models import User
    from wsgi import app
    with app.app_context():
        db.session.add(
            User(email="name@email.com", password=generate_password_hash("test"))
        )
        db.session.commit()


COMMANDS = [init_db, create_users]
