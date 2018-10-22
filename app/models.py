# app/models.py

from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from app import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model,UserMixin):
    # create a User table
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(60), index=True, unique=True)
    email = db.Column(db.String(20),unique=True,nullable=False)
    image_profile = db.Column(db.String(20),nullable=False, default='profile-default.png')
    password_hash = db.Column(db.String(128))
    lesson_id = db.Column(db.Integer, db.ForeignKey('lessons.id'))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    is_admin = db.Column(db.Boolean, default=False)

    def get_reset_token(self,expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id':self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}','{self.email}')"

# Set up user_loader
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Lesson(db.Model):
    # create a Lesson table
    __tablename__ = 'lessons'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True)
    description = db.Column(db.Text,nullable=False)
    image_banner = db.Column(db.String(20),default='banner-default.png')
    posted_date = db.Column(db.DateTime,nullable=False,default=datetime.utcnow)
    user = db.relationship('User', backref='lesson',lazy='dynamic')

    def __repr__(self):
        return f"Lesson('{self.name}')"

class Role(db.Model):
    # create a Role table
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True)
    user = db.relationship('User', backref='role',lazy='dynamic')

    def __repr__(self):
        return f"Role('{self.name}')"
