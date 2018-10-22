# app/config.py

class Config:
    SECRET_KEY = '********************************'
    SQLALCHEMY_DATABASE_URI = 'mysql://user:password@localhost/database_name'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = '******@gmail.com'
    MAIL_PASSWORD = '***************'
