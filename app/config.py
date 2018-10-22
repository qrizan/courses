# app/config.py

class Config:
    SECRET_KEY = '0e4cf9a00d41eec96d7eaf326769cc62'
    SQLALCHEMY_DATABASE_URI = 'mysql://root:q@localhost/courses_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'rizan170@gmail.com'
    MAIL_PASSWORD = 'dua5151tujuh'
