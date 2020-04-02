import uuid

from werkzeug.security import generate_password_hash
from faker import Faker

from app import app, db
from models import Product, Order, User

image_url = 'https://picsum.photos/seed/{}/100/50'


def generate_user():
    db.session.add(
        User(username='admin', password=generate_password_hash('admin')))


def generate_products():
    faker = Faker()
    for index in range(25):
        db.session.add(
            Product(name=faker.name(),
                    unit_price=100,
                    quantity=index,
                    image=image_url.format(index)))


def generate_orders():
    for index in range(2):
        order = Order(ref=str(uuid.uuid4()),
                      contact='+258848209765',
                      latitude='-25.75245',
                      longitude='17.25641')

        db.session.add(order)


if __name__ == '__main__':
    with app.app_context():
        generate_user()
        generate_products()
        generate_orders()
        db.session.commit()
