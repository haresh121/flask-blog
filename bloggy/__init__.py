from flask_mail import Mail
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from bloggy.config import Config
from bloggy.way2sms import Sms as sms

uname = 9030028799  # your phnum here
upass = 'haresh123'  # your password here
messenger = sms(uname, upass)

mail = Mail()

bcrypt = Bcrypt()
db = SQLAlchemy()
log_mngr = LoginManager()
log_mngr.login_view = 'users.login'
log_mngr.login_message_category = 'info'
from bloggy.models import User, Posts, Comments


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    from bloggy.users.routes import users
    from bloggy.posts.routes import posts
    from bloggy.main.routes import main
    from bloggy.errors.handlers import errors
    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)
    app.register_blueprint(errors)
    return app
