from flask import Flask, render_template, flash
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, PasswordField, TextAreaField
from wtforms.validators import DataRequired, Length, EqualTo
from datetime import datetime



app=Flask(__name__)
app.secret_key='this is my secret_key'
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///flask.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False
db=SQLAlchemy(app)


class Users(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(20),unique=False,nullable=False)
    username=db.Column(db.String(20),unique=True,nullable=False)
    password=db.Column(db.String(100),unique=False,nullable=False)
    location=db.Column(db.String(20),nullable=False)
    date_added=db.Column(db.DateTime,default=datetime.utcnow())
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
    @property
    def date(self):
        date=self.date_added.strftime("%d-%m-%Y")
        time=self.date_added.strftime("%H:%M:%S")
        date=dict(date=date,time=time)
        return date

class PostForm(FlaskForm):
    title=StringField('Post Title',validators=[DataRequired(),Length(min=3,max=100)])
    content=TextAreaField('Post Content',validators=[DataRequired()])
    submit=SubmitField('Add New Post')

class UserForm(FlaskForm):
    name=StringField('Name',validators=[DataRequired(),Length(min=3,max=20)])
    username=StringField('Username',validators=[DataRequired(),Length(min=3,max=20)])
    location=StringField('Location',validators=[DataRequired(),Length(min=2,max=20)])
    password=PasswordField('Password',validators=[DataRequired(),Length(min=6,max=20),EqualTo('password2',message="you most confirm your Password")])
    password2=PasswordField('Confirm Password',validators=[DataRequired(),Length(min=6,max=20)])
    submit=SubmitField('Add New User')

@app.route('/',methods=['POST','GET'])
def home():
    form = UserForm()
    postform=PostForm()
    if form.validate_on_submit():
        name=form.name.data.strip().lower().title()
        username=form.username.data
        password=form.password.data
        location=form.location.data.strip().lower().title()
        user=Users.query.filter_by(username=username).first()
        if not user:
            user=Users(name=name,username=username,location=location,password=password)
            try:
                db.session.add(user)
                db.session.commit()
                flash(f'User {name} with username {username} commited successfully to DataBase!','success')
            except:
                flash(f"Error while adding name:{name} -username:{username} to DataBase","danger")
            form.name.data=''
            form.username.data=''
            form.location.data=''
        else:
            flash(f'username:{user.username} allready Exist added by User {user.name} at {user.date}!!!','warning')
    elif postform.validate_on_submit():
        title=postform.title.data
        content=postform.content.data
        try:
            post=Posts(title=title,content=content)
            db.session.add(post)
            db.session.commit()
            flash('Post added Successfully!!!','success')
        except:
            flash(f"Error while adding current Post to DataBase", "danger")
        postform.title.data=''
        postform.content.data=''
    users=Users.query.order_by(Users.date_added)
    posts=Posts.query
    return render_template('home.html',users=users,form=form,postform=postform,posts=posts)

@app.route('/test')
def test():
    return render_template('template.html')

with app.app_context():
    db.create_all()
if __name__=='__main__':
    app.run(debug=True, port=5200)