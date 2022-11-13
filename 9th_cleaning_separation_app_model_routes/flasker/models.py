from flasker import db
from flask_login import UserMixin
from datetime import datetime


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