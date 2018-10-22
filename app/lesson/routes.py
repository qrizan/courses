# app/lesson/routes.py

from flask import render_template, url_for, redirect, flash, request, abort, Blueprint
from flask_login import current_user, login_required
from app import db
from app.models import Lesson
from app.lesson.forms import LessonForm
from app.lesson.utils import save_image_banner

lesson = Blueprint('lesson',__name__)

def check_admin():
    if not current_user.is_admin:
        abort(403)

@lesson.route('/lessons', methods=['GET', 'POST'])
@login_required
def list_lessons():
    check_admin()
    lessons = Lesson.query.all()
    return render_template('lesson/lessons.html',lessons=lessons, title="Lessons List")

@lesson.route("/lesson/add", methods=['GET','POST'])
@login_required
def add_lesson():
    check_admin()
    add_lesson = True
    form = LessonForm()
    if form.validate_on_submit():
        if form.image_banner.data:
            lesson_name = Lesson.query.filter_by(name=form.name.data).first()
            if lesson_name is None :
                image_banner = save_image_banner(form.image_banner.data)
                lesson = Lesson(name=form.name.data, description=form.description.data, image_banner = image_banner)
                try:
                    db.session.add(lesson)
                    db.session.commit()
                    flash('You have successfully', 'success')
                    return redirect(url_for('lesson.list_lessons'))
                except Exception as e:
                    print(e)
                    flash('Error:','warning')
                    return redirect(url_for('lesson.add_lesson'))
            else :
                flash('Duplicate name','warning')
        else :
            flash('Image not found','warning')
    return render_template('lesson/lesson.html', action="Add",add_lesson=add_lesson, form=form,title="Add Lesson")

@lesson.route('/lesson/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_lesson(id):
    check_admin()
    add_lesson = False
    lesson = Lesson.query.get_or_404(id)
    print(lesson)
    form = LessonForm()
    print(form)
    if form.validate_on_submit():
        if form.image_banner.data:
            image_banner = save_image_banner(form.image_banner.data)
            lesson.image_banner = image_banner
        lesson.name = form.name.data
        lesson.description = form.description.data
        db.session.commit()
        flash('You have successfully', 'success')
        return redirect(url_for('lesson.list_lessons'))

    form.description.data = lesson.description
    form.name.data = lesson.name
    return render_template('lesson/lesson.html', action="Edit",add_lesson=add_lesson, form=form,lesson=lesson, title="Edit Lesson")

@lesson.route('/lesson/<int:id>/delete', methods=['GET'])
@login_required
def delete_lesson(id):
    check_admin()
    lesson = Lesson.query.get_or_404(id)
    db.session.delete(lesson)
    db.session.commit()
    flash('You have successfully deleted the lesson.')

    return redirect(url_for('lesson.list_lessons'))
    return render_template(title="Delete Lesson")
