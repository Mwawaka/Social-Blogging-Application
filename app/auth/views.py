from flask import current_app, flash, jsonify, redirect, render_template, url_for, request
from flask_login import current_user, login_required, login_user, logout_user
import jwt
from pyparsing import wraps
from app.auth import auth
from .forms import LoginForm, RegistrationForm
from app.models import User
from app import db
from app.emails import send_email


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
        token = new_user.generate_confirmation_token()
        send_email(new_user.email, 'Confirm Your Account',
                   'auth/email/confirm', new_user=new_user, token=token)
        flash('A confirmation email has been sent to you by email', category='info')
        # flash('Successfully registered.You can now Sign In!', category='success')
        return redirect(url_for('auth.login'))
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(
                f'There was an error in creating an account: {err_msg}', category='danger')

    return render_template('auth/register.html', form=form)


@auth.route('/confirm/<token>',methods=['GET','POST'])
@login_required
def confirm(token):
    try:
        data = current_user.confirm_token(token)
        if data.get('confirm')!=current_user.id:
            flash('The confirmation link is invalid or expired!', category='danger')
        else:
             current_user.confirmed = True
             db.session.add(current_user)
             db.session.commit()
             flash('You have successfully confirmed your account', category='success')
             return redirect(url_for('main.landing'))
    except:
        flash('The confirmation link is invalid or expired!', category='danger')
    if current_user.confirmed:
       return flash('Account is already confirmed.', category='success')
       
       
    return redirect(url_for('main.index'))


@auth.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        user = User.query.filter_by(
            email=login_form.email.data
        ).first()
        if user and user.verify_password(login_password=login_form.login_password.data):
            login_user(user, login_form.remember_me)

            flash(
                f'You have successfull signed in as :{user.username}', category='success')
            # next = request.args.get('next')
            # # the original url protected from unauthorized access is stored in next query string
            # if next is None or not next.startswith('/'):
            #     # The URL in next is validated to make sure it is a relative URL
            #     next = url_for('main.index')
            #     # if next query string is not available user is then redirected to the home page
            return redirect(url_for('main.index'))
        flash(f'Invalid email or password', category='danger')

    return render_template('auth/login.html', login_form=login_form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been Signed Out!', category='info')
    return redirect(url_for('auth.login'))
