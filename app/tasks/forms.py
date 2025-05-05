from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, DateField
from wtforms.validators import DataRequired, Optional
from datetime import datetime

class TaskForm(FlaskForm):
    title = StringField('Название задачи', validators=[DataRequired()])
    description = TextAreaField('Описание', validators=[Optional()])
    status = SelectField('Статус', 
                       choices=[
                           ('open', 'Открыта'),
                           ('in_progress', 'В работе'),
                           ('completed', 'Завершена')
                       ],
                       validators=[DataRequired()])
    priority = SelectField('Приоритет',
                         choices=[
                             ('low', 'Низкий'),
                             ('medium', 'Средний'),
                             ('high', 'Высокий')
                         ],
                         validators=[DataRequired()])
    deadline = DateField('Дедлайн', format='%Y-%m-%d', validators=[Optional()])
    assignee_id = SelectField('Исполнитель', coerce=int, validators=[Optional()])