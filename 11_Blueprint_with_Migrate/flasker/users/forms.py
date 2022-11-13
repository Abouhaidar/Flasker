from wtforms.validators import DataRequired, Length, EqualTo
from wtforms import SubmitField, StringField, PasswordField
from flask_wtf import FlaskForm

class UserForm(FlaskForm):
    name=StringField('Name',validators=[DataRequired(),Length(min=3,max=20)])
    username=StringField('Username',validators=[DataRequired(),Length(min=3,max=20)])
    location=StringField('Location',validators=[DataRequired(),Length(min=2,max=20)])
    password=PasswordField('Password',validators=[DataRequired(),Length(min=6,max=20),EqualTo('password2',message="you most confirm your Password")])
    password2=PasswordField('Confirm Password',validators=[DataRequired(),Length(min=6,max=20)])
    submit=SubmitField('Add New User')
    update=SubmitField('Update User Data')

class LoginForm(FlaskForm):
    username=StringField('Username',validators=[DataRequired(),Length(min=3,max=20)])
    password=PasswordField('Password',validators=[DataRequired()])
    submit=SubmitField('Add New User')