import uuid
from random import choice, randint

from werkzeug.security import generate_password_hash
from faker import Faker

from app import app, db
from models import Product, Order, Product_Order, User

faker = Faker('pt_BR')

image_url = 'https://picsum.photos/seed/{}/100/50'

categories = [
    'Kids',
    'Dairy',
    'Others',
    'Cuisine',
    'Furniture',
]


def generate_user():
    db.session.add(
        User(username='admin', password=generate_password_hash('admin')))


def generate_products():
    for index in range(25):
        db.session.add(
            Product(name=faker.name(),
                    category=choice(categories),
                    unit_price=randint(1, 1000),
                    image=image_url.format(index)))
    db.session.commit()


def generate_orders():
    for index in range(5):
        order = Order(ref=str(uuid.uuid4()),
                      contact='+258848209765',
                      latitude='-25.971238',
                      longitude='32.571232')
        db.session.add(order)
        generate_items(order)


def generate_items(order):
    with db.session.no_autoflush:
        for index in range(10):
            item = Product_Order(quantity=randint(1, 10))
            item.product_id = (index + 1)

            order.products.append(item)


if __name__ == '__main__':
    with app.app_context():
        generate_user()
        generate_products()
        # generate_orders()
        db.session.commit()
