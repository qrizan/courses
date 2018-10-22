from flask import flash, redirect, request, render_template, url_for, Blueprint
from flask_login import login_required, current_user
from app import db, bcrypt
from app.models import User
from app.user.forms import UpdateAccountForm
from app.user.utils import save_image_profile

user = Blueprint('user',__name__)

@user.route("/account", methods=['GET','POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        print(form.image_profile.data)
        if form.image_profile.data:
            image_profile = save_image_profile(form.image_profile.data)
            current_user.image_profile = image_profile
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated','success')
        return redirect(url_for('user.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_profile = url_for('static', filename='image/profile/'+current_user.image_profile)
    return render_template('account.html', title='Account', image_profile=image_profile, form=form)

#
# @users.route("/user/<string:username>")
# @login_required
# def user_lessons(username):
#     page = request.args.get('page',1,type=int)
#     user = User.query.filter_by(username=username).first_or_404()
#     books = Book.query.filter_by(posted_by=user).order_by(Book.posted_date.desc()).paginate(page=page,per_page=5)
#     return render_template('user/books.html',books=books, user=user)
