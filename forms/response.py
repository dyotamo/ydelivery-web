from flask_wtf import FlaskForm
from wtforms import SelectField
from wtforms.validators import DataRequired


class ResponseForm(FlaskForm):
    response = SelectField(
        u'Estado',
        choices=[
            ('Aceite', 'Aceitar'),
            ('Rejeitado', 'Rejeitar'),
        ],
        validators=[DataRequired(message="Este campo é obrigatório.")])
