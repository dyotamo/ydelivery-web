from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()


class BrewOrder(db.Model):
    brew_id = db.Column(db.Integer, db.ForeignKey('brew.id'), primary_key=True)
    brew = db.relationship('Brew', back_populates='orders')
    order = db.relationship('Order', back_populates='brews')
    quantity = db.Column(db.Integer, unique=False, nullable=False)

    order_ref = db.Column(db.String,
                          db.ForeignKey('order.ref'),
                          primary_key=True)

    def __repr__(self):
        return '<Item %s, %d>' % (self.brew, self.quantity)


class Brew(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)
    unit_price = db.Column(db.Float, unique=False, nullable=False)
    available = db.Column(db.Boolean, nullable=False, default=True)
    orders = db.relationship('BrewOrder', back_populates='brew')

    def __repr__(self):
        return '<Brew %s>' % self.name


class Order(db.Model):
    ref = db.Column(db.String(10), primary_key=True)
    contact = db.Column(db.String(25), unique=False, nullable=False)
    address = db.Column(db.String(255), unique=False, nullable=False)
    status = db.Column(db.String(10),
                       unique=False,
                       nullable=False,
                       default='Pendente')

    brews = db.relationship('BrewOrder', back_populates='order')

    def __repr__(self):
        return '<Order %s>' % self.ref


class User(db.Model, UserMixin):
    ''' User model '''
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), unique=False, nullable=False)

    def __repr__(self):
        return '<User %s>' % self.username


if __name__ == '__main__':
    from app import app
    with app.app_context():
        db.create_all()
