from cmath import log
from flask import flash, redirect, render_template, url_for
from flask_login import login_user
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
        flash('Successfully registered.You can now Sign In!', category='success')
        return redirect(url_for('auth.login'))
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(
                f'There was an error in creating an account: {err_msg}', category='danger')
            
    return render_template('auth.register.html', form=form)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        user=User.query.filter_by(
            email=login_form.email.data
        ).first()
        if user and user.verify_password(login_password=login_form.login_password.data):
            login_user(user)
            flash(f'You have successfull signed in as :{user.username}')
        
    return render_template('auth/login.html', login_form=login_form)
