from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,EmailField,BooleanField,SubmitField
from wtforms.validators import DataRequired,Length,Email


class NameForm(FlaskForm):
    name=StringField(label='What is your name ?',validators=[Length(min=6,max=30),DataRequired()])
    submit=SubmitField(label='Submit')