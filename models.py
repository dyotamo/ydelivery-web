from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()


class Product_Order(db.Model):
    product_id = db.Column(db.Integer,
                           db.ForeignKey('product.id'),
                           primary_key=True)
    order_ref = db.Column(db.String,
                          db.ForeignKey('order.ref'),
                          primary_key=True)
    product = db.relationship('Product', back_populates='orders')
    order = db.relationship('Order', back_populates='products')
    quantity = db.Column(db.Integer, unique=False, nullable=False)

    def __repr__(self):
        return '<Item %s, %d>' % (self.product, self.quantity)


# Models
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    category = db.Column(db.String(80), unique=False, nullable=False)
    unit_price = db.Column(db.Float, unique=False, nullable=False)
    image = db.Column(db.String(255), unique=False, nullable=False)
    orders = db.relationship('Product_Order', back_populates='product')

    def __repr__(self):
        return '<Product %s>' % self.name


class Order(db.Model):
    ref = db.Column(db.String(80), primary_key=True)
    contact = db.Column(db.String(25), unique=False, nullable=False)
    latitude = db.Column(db.Float, unique=False, nullable=False)
    longitude = db.Column(db.Float, unique=False, nullable=False)
    status = db.Column(db.String(10),
                       unique=False,
                       nullable=False,
                       default='Pendente')
    products = db.relationship('Product_Order', back_populates='order')

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
