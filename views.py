import os
import json

from flask import (abort, flash, jsonify, redirect, render_template, request,
                   url_for)
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash

from app import app, login_manager
from forms.response import ResponseForm
from forms.upload import UploadForm
from forms.user import LoginForm, PasswordChangeForm
from models import Order, Product, Product_Order, User, db
from utils.collections import randomString
from utils.produts import get_total
from utils.telerivet import send_sms


@app.route('/', methods=['GET', 'POST'])
@app.route('/products/<int:page>', methods=['GET', 'POST'])
@login_required
def index(page=1):
    form = UploadForm()
    if form.validate_on_submit():
        from tools.file import save_csv, import_csv

        path = save_csv(form)
        with open(path, "r") as f:
            try:
                import_csv(f)
                flash("Ficheiro carregado com sucesso.", "success")
                return redirect(url_for("index"))
            except (TypeError, KeyError, UnicodeDecodeError):
                flash("Ficheiro inválido.", "warning")

    return render_template("products.html",
                           pagination=Product.query.paginate(page=page,
                                                             per_page=7),
                           form=form)


@app.route('/orders', methods=['GET'])
@login_required
def orders():
    return render_template("orders.html", orders=Order.query.all())


@app.route('/orders/<ref>', methods=['GET', 'POST'])
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
            # Fazer a diminui da quantidade dos produtos em stock
            for item in order.products:
                product = Product.query.get(item.product.id)

                db.session.add(product)
            flash("Pedido aceite.", "success")
            send_sms(
                order.contact,
                'O seu pedido foi aceite, valor de {:,.2f} Mt. Em breve '
                'faremos a entrega dos seus produtos na localização '
                'informada.\n\n'
                'Referência: {}.\n\n'
                'NB: O pagamento é feito no momento da entrega.'.format(
                    get_total(order), order.ref))
        else:
            flash("Pedido rejeitado.", "danger")
            send_sms(
                order.contact,
                'Infelizmente por razões alheias na nossa vontade '
                'não podemos satisfazer o seu pedido.\n\n'
                'Referência: {}.'.format(order.ref))

        db.session.commit()
        return redirect(url_for("orders"))

    return render_template("order.html",
                           order=order,
                           total=get_total(order),
                           form=form)


@app.route('/request', methods=['POST'])
def _request():
    body = json.loads(str(request.json).replace("'", '"'))

    order = Order(ref=str(randomString(10)),
                  contact=body['contact'],
                  latitude=body['location']['latitude'],
                  longitude=body['location']['longitude'])

    with db.session.no_autoflush:
        for product_id, quantity in body['cart'].items():
            item = Product_Order(product_id=product_id,
                                 order_ref=order.ref,
                                 quantity=quantity)
            order.products.append(item)

    db.session.add(order)
    db.session.commit()

    send_sms(os.environ['TELEPHONE_NUMBER'], 'Novo pedido feito.\n\n'
             'Referência: {}.'.format(order.ref))

    return jsonify(dict(reference=order.ref))


@app.route("/login", methods=["GET", "POST"])
def login():
    """ Login view """
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.query.filter_by(username=username).first()
        if user is None:
            flash("Credenciais inválidas.", "danger")
        else:
            if check_password_hash(user.password, password):
                login_user(user)
                flash("Entrou como {}.".format(user.username), "success")
                return redirect(url_for("index"))
            else:
                flash("Credenciais inválidas.", "danger")
    return render_template("accounts/login.html", form=form)


@app.route("/password", methods=["GET", "POST"])
@login_required
def password():
    """ Change password view """
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
                flash("Password alterado com sucesso.", "success")
                return redirect(url_for("index"))
            else:
                error = "Confirmação de password falhou."
        else:
            error = "Password corrente errado."
    return render_template("accounts/password.html", form=form, error=error)


@app.route("/logout", methods=["GET"])
@login_required
def logout():
    """ Get out here """
    logout_user()
    flash("Saiu com sucesso.", "success")
    return redirect(url_for("index"))


@login_manager.user_loader
def load_user(user_id):
    """ Current logged in user """
    return User.query.get(user_id)


# HTTP Errors views
@app.errorhandler(500)
def internal_server_error(e):
    return jsonify(
        "500 Internal Server Error, dyotamo has been reported."), 500


@app.errorhandler(403)
def forbidden(e):
    return jsonify("403 Forbidden."), 403


@app.errorhandler(404)
def page_not_found(e):
    return jsonify("404 Not Found."), 404


@app.errorhandler(405)
def method_not_allowed(e):
    return jsonify("405 Method Not Allowed."), 405
