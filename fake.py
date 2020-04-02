from werkzeug.security import generate_password_hash

from faker import Faker
from app import app, db, Product, User

image_url = 'https://picsum.photos/seed/{}/100/50'

if __name__ == '__main__':
    with app.app_context():
        faker = Faker()
        for index in range(7):
            db.session.add(
                Product(name=faker.name(),
                        unit_price=100,
                        quantity=index,
                        image=image_url.format(index)))

        db.session.add(
            User(username='admin', password=generate_password_hash('admin')))
        db.session.commit()
