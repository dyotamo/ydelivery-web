from json import loads
from os import environ

from flask import (Flask, abort, flash, jsonify, redirect, render_template,
                   request, url_for)
from flask_login import (LoginManager, current_user, login_required,
                         login_user, logout_user)
from flask_restless import APIManager
from werkzeug.security import check_password_hash, generate_password_hash

from models import db, User, Brew, Order, Brew_Order
from forms.response import ResponseForm
from forms.upload import UploadForm
from forms.user import LoginForm, PasswordChangeForm
from utils.collections import randomString
from utils.produts import get_total
from tools.file import save_csv, import_csv

app = Flask(__name__)
app.config['SECRET_KEY'] = environ.get('SECRET_KEY') or 'temp'
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get(
    'DATABASE_URL') or 'sqlite:///shop.db'

# Flask-Sqlalchemy
db.init_app(app)

# Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Deve em primeiro lugar autenticar-se.'
login_manager.login_message_category = 'warning'

# Flask-Restless
manager = APIManager(app, flask_sqlalchemy_db=db)
manager.create_api(Brew,
                   exclude_columns=['orders', 'image'],
                   results_per_page=0)
manager.create_api(Order,
                   exclude_columns=['order_ref', 'brew_id'],
                   results_per_page=0)


@app.route('/', methods=['get', 'post'])
@app.route('/brews/<int:page>', methods=['get', 'post'])
@login_required
def index(page=1):
    return render_template('products.html',
                           pagination=Brew.query.paginate(page=page,
                                                          per_page=7),
                           form=UploadForm())


@app.route('/upload', methods=['post'])
@login_required
def upload_brews():
    form = UploadForm()
    if form.validate_on_submit():
        path = save_csv(form)
        with open(path, 'r') as f:
            try:
                import_csv(f)
                flash('Ficheiro carregado com sucesso.', 'success')
            except (TypeError, KeyError, UnicodeDecodeError) as e:
                print(e)
                flash('Ficheiro inválido.', 'warning')
    return redirect(url_for('index'))


@app.route('/orders', methods=['get'])
@login_required
def orders():
    return render_template('orders.html', orders=Order.query.all())


@app.route('/orders/<ref>', methods=['get', 'post'])
@login_required
def order(ref):
    order = Order.query.get_or_404(ref)

    if order.status != 'Pendente':
        raise abort(403)

    form = ResponseForm()

    if form.validate_on_submit():
        status = form.response.data
        order.status = status
        db.session.add(order)

        if (status == 'Aceite'):
            # Fazer a diminuição da quantidade dos produtos em stock
            for item in order.brews:
                brew = Brew.query.get(item.brew.id)

                db.session.add(brew)
            flash('Pedido aceite.', 'success')
        else:
            flash('Pedido rejeitado.', 'danger')

        db.session.commit()
        return redirect(url_for('orders'))

    return render_template('order.html',
                           order=order,
                           total=get_total(order),
                           form=form)


@app.route('/request', methods=['post'])
def _request():
    body = loads(str(request.json).replace("'", '"'))
    order = Order(ref=str(randomString(10)),
                  contact=body['contact'],
                  latitude=body['location']['latitude'],
                  longitude=body['location']['longitude'])

    with db.session.no_autoflush:
        for brew_id, quantity in body['cart'].items():
            item = Brew_Order(brew_id=brew_id,
                              order_ref=order.ref,
                              quantity=quantity)
            order.brews.append(item)
    db.session.add(order)
    db.session.commit()
    return jsonify(dict(reference=order.ref))


@app.route('/login', methods=['get', 'post'])
def login():
    ''' Login view '''
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.query.filter_by(username=username).first()
        if user is None:
            flash('Credenciais inválidas.', 'danger')
        else:
            if check_password_hash(user.password, password):
                login_user(user)
                flash('Entrou como {}.'.format(user.username), 'success')
                return redirect(url_for('index'))
            else:
                flash('Credenciais inválidas.', 'danger')
    return render_template('accounts/login.html', form=form)


@app.route('/password', methods=['get', 'post'])
@login_required
def password():
    ''' Change password view '''
    error = None
    form = PasswordChangeForm()

    if form.validate_on_submit():
        current_password = form.current_password.data
        new_password = form.new_password.data
        confirm_new_password = form.confirm_new_password.data

        if check_password_hash(current_user.password, current_password):
            if new_password == confirm_new_password:
                current_user.password = generate_password_hash(new_password)
                db.session.add(current_user)
                db.session.commit()
                flash('Password alterado com sucesso.', 'success')
                return redirect(url_for('index'))
            else:
                error = 'Confirmação de password falhou.'
        else:
            error = 'Password corrente errada.'
    return render_template('accounts/password.html', form=form, error=error)


@app.route('/logout', methods=['get'])
@login_required
def logout():
    ''' get out here '''
    logout_user()
    flash('Saiu com sucesso.', 'success')
    return redirect(url_for('index'))


@login_manager.user_loader
def load_user(user_id):
    ''' Current logged in user '''
    return User.query.get(user_id)


# HTTP Errors views
@app.errorhandler(500)
def internal_server_error(e):
    return jsonify(
        '500 Internal Server Error, dyotamo has been reported.'), 500


@app.errorhandler(403)
def forbidden(e):
    return jsonify('403 Forbidden.'), 403


@app.errorhandler(404)
def page_not_found(e):
    return jsonify('404 Not Found.'), 404


@app.errorhandler(405)
def method_not_allowed(e):
    return jsonify('405 Method Not Allowed.'), 405


@app.after_request
def add_cors(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
