from flask_wtf import FlaskForm
from wtforms import TextField, PasswordField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    username = TextField(
        'Usuário',
        validators=[DataRequired(message="Este campo é obrigatório.")])
    password = PasswordField(
        'Password',
        validators=[DataRequired(message="Este campo é obrigatório.")])


class PasswordChangeForm(FlaskForm):
    current_password = PasswordField(
        'Password corrente',
        validators=[DataRequired(message="Este campo é obrigatório.")])
    new_password = PasswordField(
        'Password nova',
        validators=[DataRequired(message="Este campo é obrigatório.")])
    confirm_new_password = PasswordField(
        'Password nova',
        validators=[DataRequired(message="Este campo é obrigatório.")])
