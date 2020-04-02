from flask import render_template, jsonify, flash, redirect, url_for
from flask_login import login_required, login_user, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from app import app, login_manager
from models import db, Product, Order, User
from forms.upload import UploadForm
from forms.user import LoginForm, PasswordChangeForm


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
                           products=Product.query.all(),
                           form=form)


@app.route('/orders', methods=['GET'])
@login_required
def orders():
    return render_template("orders.html", orders=Order.query.all())


@app.route('/orders/<ref>', methods=['GET', 'POST'])
@login_required
def order(ref):
    order = Order.query.get_or_404(ref)

    form = UploadForm()

    if form.validate_on_submit():
        flash("Estado da compra alterado com sucesso.", "success")
        return redirect(url_for("orders"))

    return render_template("orders.html", order=order, form=form)


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


@app.errorhandler(404)
def page_not_found(e):
    return jsonify("404 Not Found.")


@app.errorhandler(405)
def method_not_allowed(e):
    return jsonify("405 Method Not Allowed.")
