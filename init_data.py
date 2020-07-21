from random import randint

from bs4 import BeautifulSoup
from werkzeug.security import generate_password_hash

from app import app, db
from models import Product, User


class CategoryModel:
    def __init__(self, name):
        self.name = name
        self.products = []

    def __repr__(self):
        return self.name + str(self.products)


class ProductModel:
    def __init__(self, name):
        self.name = name
        self.unit_price = randint(1, 10000)

    def __repr__(self):
        return self.name


def parse():
    categories = []

    soup_obj = BeautifulSoup(open('fixture/foods.html'), "html.parser")

    for cat in soup_obj.find_all('ul'):
        category = CategoryModel(name=cat['class'][0].capitalize())
        for prod in cat.find_all('li'):
            product = ProductModel(name=prod.text.strip())
            category.products.append(product)
        categories.append(category)
    return categories


def _generate_user():
    db.session.add(
        User(username='admin', password=generate_password_hash('admin')))


def _generate_products(categories):
    for cat in categories:
        for prod in cat.products:
            product = Product(name=prod.name,
                              category=cat.name,
                              unit_price=prod.unit_price)
            db.session.add(product)


if __name__ == '__main__':
    with app.app_context():
        _generate_user()
        _generate_products(parse())
        db.session.commit()
