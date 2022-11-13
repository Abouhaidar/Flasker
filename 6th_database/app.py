from flask import Flask, request,render_template, flash
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, IntegerField
from wtforms.validators import DataRequired, Length
from datetime import datetime


app=Flask(__name__)
app.secret_key='this is my secret_key'
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///flask.db"
# app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False
db=SQLAlchemy(app)


class Users(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(20),unique=True,nullable=False)
    location=db.Column(db.String(20),nullable=False)
    date_added=db.Column(db.DateTime,default=datetime.utcnow())
    @property
    def date(self):
        date=self.date_added.strftime("%d-%m-%Y")
        time=self.date_added.strftime("%H:%M:%S")
        date=dict(date=date,time=time)
        return date

class UserForm(FlaskForm):
    name=StringField('Username',validators=[DataRequired(),Length(min=3,max=20)])
    location=StringField('Location',validators=[DataRequired(),Length(min=2,max=20)])
    submit=SubmitField('Add New User')

@app.route('/',methods=['POST','GET'])
def home():
    form = UserForm()
    if form.validate_on_submit():
        name=form.name.data.strip().lower().title()
        location=form.location.data.strip().lower().title()
        user=Users.query.filter_by(name=name).first()
        if not user:
            user=Users(name=name,location=location)
            try:
                db.session.add(user)
                db.session.commit()
                flash(f'User {name} commited successfully to DataBase!','success')
            except:
                flash(f"Error while adding {name} to DataBase","danger")
            form.name.data=''
            form.location.data=''
        else:
            flash(f'User {user.name} from {user.location} allready Exist added at {user.date}!!!','warning')
    users=Users.query.order_by(Users.date_added)
    return render_template('home.html',users=users,form=form)

@app.route('/test')
def test():
    return render_template('template.html')

with app.app_context():
    db.create_all()
if __name__=='__main__':
    app.run(debug=True, port=5150)