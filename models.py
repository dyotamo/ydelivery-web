from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

items = db.Table(
    'items',
    db.Column('product_id',
              db.Integer,
              db.ForeignKey('product.id'),
              primary_key=True),
    db.Column('order_ref',
              db.Integer,
              db.ForeignKey('order.ref'),
              primary_key=True),
    db.Column('quantity', db.Integer(), unique=False, nullable=False))


# Models
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    unit_price = db.Column(db.Float, unique=False, nullable=False)
    quantity = db.Column(db.Integer, unique=False, nullable=False)
    image = db.Column(db.String(255), unique=False, nullable=False)

    def __repr__(self):
        return '<Product %s>' % self.name


class Order(db.Model):
    ref = db.Column(db.String(25), primary_key=True)
    contact = db.Column(db.String(25), unique=False, nullable=False)
    latitude = db.Column(db.Float, unique=False, nullable=False)
    longitude = db.Column(db.Float, unique=False, nullable=False)
    amount = db.Column(db.Float, unique=False, nullable=False)
    status = db.Column(db.String(10),
                       unique=True,
                       nullable=False,
                       default='pending')
    items = db.relationship('Product',
                            secondary=items,
                            lazy='subquery',
                            backref=db.backref('items', lazy=True))

    def __repr__(self):
        return '<Order %s>' % self.ref


class User(db.Model, UserMixin):
    """ User model """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), unique=False, nullable=False)

    def __repr__(self):
        return "<User %s>" % self.institution


if __name__ == "__main__":
    from app import app
    with app.app_context():
        db.create_all()
