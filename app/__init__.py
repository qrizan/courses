# app/__init__.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from app.config import Config

# variable initialization
db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = "auth.login"
login_manager.login_message = "You must be logged in to access this page."
mail = Mail()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    from app.auth.routes import auth
    from app.main.routes import main
    from app.admin.routes import admin
    from app.lesson.routes import lesson
    from app.user.routes import user
    from app.error.handlers import error

    app.register_blueprint(auth)
    app.register_blueprint(main)
    app.register_blueprint(admin)
    app.register_blueprint(lesson)
    app.register_blueprint(user)
    app.register_blueprint(error)

    return app
