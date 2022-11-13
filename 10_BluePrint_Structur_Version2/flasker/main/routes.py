from flask import Blueprint
from flask import render_template
from flasker.models import Users, Posts

mainapp=Blueprint('mainapp',__name__)

@mainapp.route('/')
@mainapp.route('/home')
def home():
    users=Users.query.order_by(Users.date_added)
    posts=Posts.query
    return render_template('home.html',users=users,posts=posts)
