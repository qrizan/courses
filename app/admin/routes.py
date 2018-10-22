# app/admin/routes.py

from flask import render_template, url_for, redirect, flash, request, abort, Blueprint
from flask_login import current_user, login_required
from app import db
from app.models import Role, User
from app.admin.forms import RoleForm, UserAssignForm

admin = Blueprint('admin',__name__)

def check_admin():
    if not current_user.is_admin:
        abort(403)

@admin.route('/dashboard')
@login_required
def dashboard():
    # render the dashboard template
    return render_template('admin/dashboard.html', title="Dashboard")

@admin.route('/roles')
@login_required
def list_roles():
    check_admin()
    roles = Role.query.all()
    return render_template('admin/role/roles.html', roles=roles, title='Roles')

@admin.route('/roles/add', methods=['GET', 'POST'])
@login_required
def add_role():
    check_admin()
    add_role = True
    form = RoleForm()
    if form.validate_on_submit():
        role = Role(name=form.name.data)
        try:
            db.session.add(role)
            db.session.commit()
            flash('You have successfully added a new role.')
        except Exception as e:
            flash('Error:')

        return redirect(url_for('admin.list_roles'))
    return render_template('admin/role/role.html', add_role=add_role,form=form, title='Add Role')

@admin.route('/roles/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_role(id):
    check_admin()
    add_role = False
    role = Role.query.get_or_404(id)
    form = RoleForm(obj=role)
    if form.validate_on_submit():
        role.name = form.name.data
        try:
            db.session.add(role)
            db.session.commit()
            flash('You have successfully edited the role.')
            return redirect(url_for('admin.list_roles'))
        except Exception as e:
            flash('Error:')

    form.name.data = role.name
    return render_template('admin/role/role.html', add_role=add_role,form=form, title="Edit Role")

@admin.route('/roles/<int:id>/delete', methods=['GET', 'POST'])
@login_required
def delete_role(id):
    check_admin()
    role = Role.query.get_or_404(id)
    db.session.delete(role)
    db.session.commit()
    flash('You have successfully deleted the role.')

    return redirect(url_for('admin.list_roles'))
    return render_template(title="Delete Role")

@admin.route('/users')
@login_required
def list_users():
    check_admin()
    users = User.query.all()
    return render_template('admin/user/users.html', users=users, title='Users')

@admin.route('/user/<int:id>/assign', methods=['GET', 'POST'])
@login_required
def assign_user(id):
    check_admin()
    user = User.query.get_or_404(id)
    if user.is_admin:
        abort(403)

    form = UserAssignForm()
    if form.validate_on_submit():
        user.lesson = form.lesson.data
        user.role = form.role.data
        db.session.add(user)
        db.session.commit()
        flash('You have successfully assigned a department and role.')

        # redirect to the roles page
        return redirect(url_for('admin.list_users'))

    return render_template('admin/user/assign.html',user=user, form=form,title='Assign User')
