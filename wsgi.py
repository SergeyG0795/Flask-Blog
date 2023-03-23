from blog.app import app
from blog.models.database import db

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        debug=True,
    )


@app.cli.command('init-db')
def init_db():
    db.create_all()
    print('Done!')


@app.cli.command('create-users')
def create_users():
    from blog.models import User

    admin = User(username='admin', is_staff=True)
    james = User(username='James')
    with app.app_context():
        db.session.add(admin)
        db.session.add(james)
        db.session.commit()

    print('Done!')
