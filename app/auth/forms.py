# app/auth/forms.py

from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import PasswordField, StringField, SubmitField, ValidationError, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, Length
from app.models import User


class RegistrationForm(FlaskForm):
    # Form for users to create new account
    email = StringField('Email',validators=[DataRequired(),Email(),Length(min=5,max=30)])
    username = StringField('Username', validators=[DataRequired(),Length(min=5,max=30)])
    password = PasswordField('Password',validators=[DataRequired(), Length(min=5,max=20)])
    confirm_password = PasswordField('Confirm Password',validators=[DataRequired(), EqualTo('password'), Length(min=5,max=20)])
    submit = SubmitField('Register')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email is already in use.')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username is already in use.')


class LoginForm(FlaskForm):
    # form users to login
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class RequestResetForm(FlaskForm):
    email = StringField('Email',validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account with that email. You must register first')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password',validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',validators=[DataRequired(), EqualTo('password'), Length(min=5,max=20)])
    submit = SubmitField('Request Password Reset')
