
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import Form, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length
from wtforms.ext.sqlalchemy.fields import QuerySelectField

from app.models import Lesson, Role

class RoleForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=5,max=50)])
    submit = SubmitField('Submit')

class UserAssignForm(FlaskForm):
    lesson = QuerySelectField(query_factory=lambda: Lesson.query.all(),get_label="name")
    role = QuerySelectField(query_factory=lambda: Role.query.all(),get_label="name")
    submit = SubmitField('Submit')
