from flasker import db, login_manager
from flask_login import UserMixin
from datetime import datetime

# from flask import current_app
###anstelle ovn app soll jetzt current_app verwindet

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

class Users(db.Model,UserMixin):
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(20),unique=False,nullable=False)
    username=db.Column(db.String(20),unique=True,nullable=False)
    password=db.Column(db.String(100),unique=False,nullable=False)
    location=db.Column(db.String(20),nullable=False)
    date_added=db.Column(db.DateTime,default=datetime.utcnow())
    posts=db.relationship('Posts',backref='creater',lazy=True)
    @property
    def date(self):
        date=self.date_added.strftime("%d-%m-%Y")
        time=self.date_added.strftime("%H:%M:%S")
        date=dict(date=date,time=time)
        return date

class Posts(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    title=db.Column(db.String(100),unique=False,nullable=False)
    content=db.Column(db.String(500),unique=True,nullable=False)
    date_added=db.Column(db.DateTime,default=datetime.utcnow())
    user_id=db.Column(db.Integer,db.ForeignKey('users.id'),nullable=False)
    @property
    def date(self):
        date=self.date_added.strftime("%d-%m-%Y")
        time=self.date_added.strftime("%H:%M:%S")
        date=dict(date=date,time=time)
        return date