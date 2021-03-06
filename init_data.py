from werkzeug.security import generate_password_hash

from app import app, db
from models import User


def _generate_user():
    db.session.add(
        User(
            username='dyotamo',
            password=generate_password_hash('passwd'),
        ))


if __name__ == '__main__':
    with app.app_context():
        _generate_user()
        db.session.commit()
