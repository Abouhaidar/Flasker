from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flasker.config import Config

login_manager = LoginManager()
login_manager.login_view = 'usersapp.login'
login_manager.login_message_category='info'
db=SQLAlchemy()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    login_manager.init_app(app)
    db.init_app(app)
    with app.app_context():
        db.create_all()
    from flasker.main.routes import mainapp
    from flasker.users.routes import usersapp
    from flasker.posts.routes import postsapp
    from flasker.errors.errorhandler import errors
    app.register_blueprint(errors)
    app.register_blueprint(mainapp)
    app.register_blueprint(usersapp)
    app.register_blueprint(postsapp)
    return app