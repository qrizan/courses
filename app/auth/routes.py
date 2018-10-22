# app/auth/routes.py

from flask import flash, redirect, request, render_template, url_for, Blueprint
from flask_login import login_required, login_user, logout_user, current_user
from app import db, bcrypt
from app.auth.forms import LoginForm, RegistrationForm, RequestResetForm, ResetPasswordForm
from app.models import User
from app.auth.utils import send_reset_email

auth = Blueprint('auth',__name__)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    # add an User to the database through the registration form
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(email=form.email.data,username=form.username.data,password_hash=hashed_password)
        try:
            db.session.add(user)
            db.session.commit()
            flash('You have successfully registered! You may now login.', 'success')
            return redirect(url_for('auth.login'))
        except Exception as e:
            flash('You have unsuccessfully registered','warning')
            return redirect(url_for('auth.register'))
    return render_template('auth/register.html', form=form, title='Register')


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and bcrypt.check_password_hash(user.password_hash, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            # redirect to the appropriate dashboard page
            if user.is_admin:
                return redirect(next_page) if next_page else redirect(url_for('admin.dashboard'))
            else:
                return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('Login Unsuccessful. Please check email and password','danger')
    return render_template('auth/login.html', form=form, title='Login')


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have successfully been logged out.')
    return redirect(url_for('auth.login'))


@auth.route("/reset_password", methods=['GET','POST'])
def reset_password():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email hae been with instructions to reset your password','info')
        return redirect(url_for('main.home'))
    return render_template('auth/reset_password.html',title='Reset Password', form=form)


@auth.route("/reset_password/<token>", methods=['GET','POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token','warning')
        return redirect(url_for('user.reset_password'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password_hash = hashed_password
        try:
            db.session.commit()
            flash('Your password has been update! You are now able to log in', 'success')
            return redirect(url_for('auth.login'))
        except Exception as e:
            flash('Your password unsuccessfully updated','warning')
            return redirect(url_for('auth.reset_password'))
    return render_template('auth/reset_token.html',title='Reset Token', form=form)
