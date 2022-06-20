from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,EmailField,BooleanField,SubmitField,TextAreaField
from wtforms.validators import DataRequired,Length,Email


class NameForm(FlaskForm):
    name=StringField(label='What is your name ?',validators=[Length(min=6,max=30),DataRequired()])
    submit=SubmitField(label='Submit')
class EditProfileForm(FlaskForm):
    name=StringField(label='Real Name :',validators=[DataRequired(),Length(min=6,max=30)])
    location=StringField(label='Location',validators=[DataRequired(),Length(min=6,max=60)])
    about_me=TextAreaField(label='About me :')
    submit=SubmitField(label='Edit Profile')