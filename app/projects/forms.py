from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, TextAreaField, URLField
from wtforms.validators import DataRequired, Optional

class ProjectForm(FlaskForm):
    title = StringField('Название проекта', validators=[DataRequired()])
    description = TextAreaField('Описание', validators=[Optional()])
    project_url = URLField('Ссылка на проект', validators=[Optional()])
    cover_image = FileField('Обложка проекта', validators=[
        FileAllowed(['jpg', 'jpeg', 'png'], 'Только изображения!')
    ])

from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField
from wtforms.validators import DataRequired, Optional, URL

class DocumentForm(FlaskForm):
    name = StringField('Название документа', validators=[DataRequired()])
    file = FileField('Файл', validators=[
        Optional(),
        FileAllowed(['pdf', 'doc', 'docx', 'xls', 'xlsx', 'jpg', 'png'], 'Разрешены только документы и изображения')
    ])
    url = StringField('Или ссылка на документ', validators=[
        Optional(),
        URL(message='Некорректный URL адрес')
    ])