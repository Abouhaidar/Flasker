from flask import Flask, request,render_template, flash
# pip install flask-wtf
from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, IntegerField
from wtforms.validators import DataRequired, Length
import pandas as pd
app=Flask(__name__)
app.secret_key='bm'

class UserForm(FlaskForm):
    name=StringField('Username',validators=[DataRequired(),Length(min=3,max=20)])
    age=IntegerField('Age',validators=[DataRequired()])
    location=StringField('Location',validators=[DataRequired(),Length(min=2,max=20)])
    submit=SubmitField('Add New User')


##using Flask Form
## to get flashed messages in HTMl you need secret_key
## return Template wiith input data, and return some logic text
@app.route('/',methods=['POST','GET'])
def home():
    form = UserForm()
    ###use can use open(file.csv) in read modus and redlines users output=  list in list
    ### add user list append new list and to save data openfile then writeline --> save csv file
    users=pd.read_csv('data/users.csv')
    if request.method=='POST':
        name=form.name.data.strip().lower()
        age=form.age.data
        location=form.location.data.strip().lower()
        if name and name!='':
            if name not in users.name.tolist():
                users=users.append(dict(name=name,age=age,location=location), ignore_index=True)
                users.to_csv('data/users.csv',index=False)
                flash(f'User {name} added successfully to CSV File!!!!','success')
            else:
                flash(f'User {name} allready Exist!!!','danger')
            form.name.data=''
            form.age.data=''
            form.location.data=''
    return render_template('home.html',users=users,form=form)

@app.route('/test')
def test():
    return render_template('template.html')

if __name__=='__main__':
    app.run(debug=True, port=5050)