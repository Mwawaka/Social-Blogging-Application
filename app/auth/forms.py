from email import message
from flask_wtf import  FlaskForm
from wtforms import StringField,PasswordField,EmailField,BooleanField,SubmitField
from wtforms.validators import DataRequired,Length,EqualTo,Email

class RegistrationForm(FlaskForm):
    username=StringField(label='Username :',validators=[DataRequired(),Length(min=6,max=30)])
    email=EmailField(label='Email Address:',validators=[DataRequired(),Email()])
    password1=PasswordField(label='Password :')
    password2=PasswordField(label=' Password :',validators=[DataRequired(),EqualTo(password1)])
    submit=SubmitField(label='Register')