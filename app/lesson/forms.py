from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, Email

class LessonForm(FlaskForm):
    name = StringField('Title',validators=[DataRequired(), Length(min=5,max=50)])
    description = TextAreaField('Content',validators=[DataRequired(), Length(min=5)])
    image_banner = FileField('Profile Picture', validators=[FileAllowed(['jpg','png'])])
    submit = SubmitField('Post')
