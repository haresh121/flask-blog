import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
#    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_DATABASE_URI = "sqlite:///site.db"
    MAIL_SERVER='smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USERNAME = os.environ.get('G_USERNAME')
    MAIL_PASSWORD = os.environ.get('G_PASS')
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    TEMPLATE_AUTO_RELOAD = True