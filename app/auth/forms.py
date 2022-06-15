from operator import sub
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo, Email, ValidationError
from app.models import User


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

    def validate_username(self, field):
        user = User.query.filter_by(username=field.data).first()
        if user:
            raise ValidationError(
                'Username already exist!Please try a different one.')

    def validate_email(self, field):
        user = User.query.filter_by(email=field.data).first()
        if user:
            raise ValidationError(
                'Email already exist!Please try a different one')


class LoginForm(FlaskForm):
    email = EmailField(label='Email Address :', validators=[
                       DataRequired(), Email()])
    login_password = PasswordField(
        label='Password :', validators=[DataRequired()])
    remember_me = BooleanField(label='Keep me signed in')
    submit = SubmitField(label='Sign In')


class ChangePassword(FlaskForm):
    old_password = PasswordField(
        label='Current Password :', validators=[DataRequired()])
    new_password = PasswordField(label='New Password', validators=[
                                 DataRequired(), Length(min=6)])
    submit = SubmitField(label='Change Password')


class ChangeEmail(FlaskForm):
    new_email = EmailField(label='New Email :', validators=[
                           DataRequired(), Email()])
    password = PasswordField(label='Password :', validators=[DataRequired()])
    submit = SubmitField(label='Change Email')

    def validate_email(self, field):
        user = User.query.filter_by(email=field.data).first()
        if user:
            raise ValidationError(
                'Email already exist!Please try a different one')


class PasswordResetRequestForm(FlaskForm):
    email = EmailField(label='Email Address :', validators=[
                       DataRequired(), Email()])
    submit = SubmitField(label='Reset Password')


class PasswordResetForm(FlaskForm):
    password1 = PasswordField(label='Password :', validators=[
                              Length(min=6), DataRequired()])
    password2 = PasswordField(label='Password :', validators=[
                              DataRequired(), EqualTo('password1')])
    submit = SubmitField(label='Reset Password')
