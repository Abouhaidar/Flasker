from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os
basedir = os.path.abspath(os.path.join('../', os.path.dirname(__file__)))
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'database/app.db')

app=Flask(__name__)
app.secret_key='this is my secret_key'
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///flask.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False

# Setting Login
login_manager = LoginManager(app)
login_manager.login_view = 'usersapp.login'
login_manager.login_message_category='info'

##############################
db=SQLAlchemy(app)
with app.app_context():
    db.create_all()
from flasker.main.routes import mainapp
from flasker.users.routes import usersapp
from flasker.posts.routes import postsapp
app.register_blueprint(mainapp)
app.register_blueprint(usersapp)
app.register_blueprint(postsapp)

