import email
from flask import flash, redirect, render_template, url_for
from app.auth import auth
from .forms import LoginForm, RegistrationForm
from app.models import User
from app import db


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        new_user = User(
            username=form.username.data,
            email=form.email.data,
            password=form.password1.data
        )
        db.session.add(new_user)
        db.session.commit()
        flash('Successfully registered.You can now Sign In!', category='info')
        redirect(url_for('auth/login'))
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(
                f'There was an error in creating an account: {err_msg}', category='danger')
    return render_template('auth/register.html', form=form)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    return render_template('auth/login.html', login_form=login_form)
