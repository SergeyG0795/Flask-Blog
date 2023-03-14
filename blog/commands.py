from blog.app import app

from blog.models.database import db


@app.cli.command('init-db')
def init_db():
    from wsgi import app

    db.create_all(app=app)
    print('Done!')


@app.cli.command('create-users')
def create_users():
    from blog.models import User
    from wsgi import app

    admin = User(username='admin', is_staff=True)
    james = User(username='James')
    with app.app_context():
        db.session.add(admin)
        db.session.add(james)
        db.session.commit()

    print('Done!')
