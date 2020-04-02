from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired


class UploadForm(FlaskForm):
    csv = FileField('Arquivo CSV', validators=[FileRequired()])