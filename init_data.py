from bs4 import BeautifulSoup
from werkzeug.security import generate_password_hash

from app import app, db
from models import Brew, User


class BrewModel:
    def __init__(self, name, unit_price):
        self.name = name
        self.unit_price = unit_price

    def __repr__(self):
        return self.name


def parse():
    brews = []
    with open('fixture/brew.html') as fixture:
        soup_obj = BeautifulSoup(fixture, 'html.parser')
        for brew in soup_obj.find_all('brew'):
            brews.append(
                BrewModel(
                    name=brew.text.strip(),
                    unit_price=float(brew['unit_price']),
                ))
        return brews


def _generate_user():
    db.session.add(
        User(
            username='admin',
            password=generate_password_hash('admin'),
        ))


def _generate_brews(brews):
    for prod in brews:
        db.session.add(Brew(
            name=prod.name,
            unit_price=prod.unit_price,
        ))


if __name__ == '__main__':
    with app.app_context():
        _generate_user()
        _generate_brews(parse())
        db.session.commit()
