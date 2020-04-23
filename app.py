from os import environ

from flask import Flask
from flask_login import LoginManager
from flask_restless import APIManager

from models import db, Product, Order

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get(
    'DATABASE_URL') or 'sqlite:///shop.db'
app.config['SECRET_KEY'] = environ.get('SECRET_KEY') or 'temp'

db.init_app(app)

login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.login_message = "Deve em primeiro lugar autenticar-se."
login_manager.login_message_category = "warning"

# Create the Flask-Restless API manager.
manager = APIManager(app, flask_sqlalchemy_db=db)
manager.create_api(Product, exclude_columns=['orders'], results_per_page=0)
manager.create_api(Order,
                   exclude_columns=['order_ref', 'product_id'],
                   results_per_page=0)

from views import *

if __name__ == '__main__':
    app.run(debug=True)
