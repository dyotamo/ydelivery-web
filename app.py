from flask import Flask
from flask_login import LoginManager

from models import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shop.db'
app.config['SECRET_KEY'] = 'temp'

db.init_app(app)

login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.login_message = "Deve em primeiro lugar autenticar-se."
login_manager.login_message_category = "warning"

from views import *

if __name__ == '__main__':
    app.run(debug=True)
