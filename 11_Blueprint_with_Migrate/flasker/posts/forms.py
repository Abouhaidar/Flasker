from wtforms.validators import DataRequired, Length
from wtforms import SubmitField, StringField, TextAreaField
from flask_wtf import FlaskForm

class PostForm(FlaskForm):
    title=StringField('Post Title',validators=[DataRequired(),Length(min=3,max=100)])
    subject=StringField('Post Subject',validators=[DataRequired(),Length(min=2,max=50)])
    content=TextAreaField('Post Content',validators=[DataRequired()])
    submit=SubmitField('Add New Post')
    update=SubmitField('update post')