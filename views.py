from flask import render_template, jsonify, flash, redirect, url_for, abort
from flask_login import login_required, login_user, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import sqlalchemy

from app import app, login_manager
from models import db, Product, Order, User
from forms.upload import UploadForm
from forms.response import ResponseForm
from forms.user import LoginForm, PasswordChangeForm
from utils.produts import get_total


@app.route('/', methods=['GET', 'POST'])
@login_required
def index():
    form = UploadForm()
    if form.validate_on_submit():
        from tools.file import save_csv, import_csv

        path = save_csv(form)
        with open(path, "r") as f:

            try:
                import_csv(f)
                flash("Ficheiro carregado com sucesso.", "success")
                return redirect(url_for("index"))
            except TypeError:
                flash("Ficheiro inválido.", "warning")

    return render_template("products.html",
                           products=Product.query.order_by(
                               sqlalchemy.text('name')),
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
        else:
            flash("Pedido rejeitado.", "danger")

        db.session.commit()
        return redirect(url_for("orders"))

    return render_template("order.html",
                           order=order,
                           total=get_total(order),
                           form=form)


@app.route('/request', methods=['POST'])
def request_(ref):
    pass


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
    return jsonify("500 Internal Server Error, dyotamo has been reported.")


@app.errorhandler(403)
def forbidden(e):
    return jsonify("403 Forbidden.")


@app.errorhandler(404)
def page_not_found(e):
    return jsonify("404 Not Found.")


@app.errorhandler(405)
def method_not_allowed(e):
    return jsonify("405 Method Not Allowed.")
