from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo, Email


class RegistrationForm(FlaskForm):
    username = StringField(label='Username :', validators=[
                           DataRequired(), Length(min=2, max=30)])
    email = EmailField(label='Email Address:', validators=[
                       DataRequired(), Email()])
    password1 = PasswordField(label='Password :', validators=[
                              DataRequired(), Length(min=6)])
    password2 = PasswordField(label=' Password :', validators=[
                              DataRequired(), EqualTo('password1')])
    submit = SubmitField(label='Create Account')


class LoginForm(FlaskForm):
    email = EmailField(label='Email Address :', validators=[
                       DataRequired(), Email()])
    login_password = PasswordField(
        label='Password :', validators=[DataRequired()])
    remember_me = BooleanField(label='Keep me signed in')
    submit = SubmitField(label='Sign In')
    
class ChangePassword(FlaskForm):
    old_password=PasswordField(label='Current Password :',validators=[DataRequired()])
    new_password=PasswordField(label='New Password',validators=[DataRequired(),Length(min=6)])
    submit=SubmitField(label='Change Password')

class ChangeEmail(FlaskForm):
    old_email=PasswordField(label='Current Email :',validators=[DataRequired()])
    new_email=PasswordField(label='New Email',validators=[DataRequired(),Email()])
    submit=SubmitField(label='Change Email')