from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__)
app.secret_key='this is my secret_key'
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///flask.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False
db=SQLAlchemy(app)
from flasker import routes

