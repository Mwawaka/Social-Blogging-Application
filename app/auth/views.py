from crypt import methods
from curses import reset_shell_mode
from re import I
from flask import flash,  redirect, render_template, url_for, request
from flask_login import current_user, login_required, login_user, logout_user
from app.auth import auth
from .forms import ChangeEmail, ChangePassword, LoginForm, PasswordResetRequestForm, RegistrationForm, PasswordResetForm
from app.models import User
from app import db
from app.emails import send_email

# registers a function to run before each request


@auth.before_app_request
def before_request():
    if current_user.is_authenticated and not current_user.confirmed and request.blueprint != 'auth' and request.endpoint != 'static':
        return redirect(url_for('auth.unconfirmed'))


# Route that deals with users who have not confirmed their accounts
@auth.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.landing'))
    return render_template('auth/unconfirmed.html')


# Registration
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


# route to hanlde account confirmation
@auth.route('/confirm/<token>', methods=['GET', 'POST'])
@login_required
def confirm(token):
    if current_user.confirmed:
        flash('Account has already been confirmed', category='success')
        return redirect(url_for('main.landing'))

    user = User.confirm_token(token)
    if user is None:
        flash('The confirmation link is invalid or has already expired',
              category='info')
        return redirect(url_for('auth.unconfirmed'))
    user.confirmed = True
    db.session.add(user)
    db.session.commit()
    flash('You have successfully confirmed your account', category='success')
    return redirect(url_for('main.landing'))


# Resending confirmation email
@auth.route('/confirm')
@login_required
def resend_confirmation_email():
    token = current_user.generate_confirmation_token()
    send_email(current_user.email, 'Confirm Your Account',
               'auth/email/confirm', new_user=current_user, token=token)
    flash('A new confirmation email has been sent to you by email', category='info')
    return redirect(url_for('auth.unconfirmed'))


# Login
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
            return redirect(url_for('main.landing'))
        flash(f'Invalid email or password', category='danger')

    return render_template('auth/login.html', login_form=login_form)


# Changing password
@auth.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    change_password = ChangePassword()
    if change_password.validate_on_submit():
        if current_user.verify_password(change_password.old_password.data):
            current_user.password = change_password.new_password.data
            db.session.add(current_user)
            db.session.commit()
            flash('Successfully changed your password', category='success')
            return redirect(url_for('main.landing'))
        else:
            flash('Invalid Password!', category='success')

    return render_template('auth/change_password.html', change_password=change_password)


# Changing Email
# Requires a confirmation Token
@auth.route('/change_email', methods=['GET', 'POST'])
@login_required
def change_email_request():
    change_email = ChangeEmail()
    if change_email.validate_on_submit():
        if current_user.verify_password(change_email.password.data):
            new_email = change_email.new_email.data
            token = current_user.confirmation_email_token(new_email)
            send_email(new_email, 'Confirm your new email ',
                       'auth/email/changed_email', user=current_user, token=token)
            flash('An email containing a confirmation link has been send to your mailtrap address', category='success')
            return redirect(url_for('main.landing'))
        else:
            flash('Invalid email or password.', category='danger')
    return render_template('auth/change_email.html', change_email=change_email)


# route that handles the change email token
@auth.route('/change_email/<token>', methods=['GET', 'POST'])
def change_email(token):
    email, user = User.confirm_email_token(token)
    if user is None:
        flash('The confirmation link is invalid or has expired', category='danger')
        return redirect(url_for('main.landing'))
    user.email = email
    db.session.add(user)
    db.session.commit()
    flash('Email has successfully been changed.', category='success')
    return redirect(url_for('main.landing'))


# Request for password reset
@auth.route('/reset_password', methods=['GET', 'POST'])
def reset_password_request():
    if not current_user.is_anonymous:
        return redirect(url_for('main.landing'))
    reset_form = PasswordResetRequestForm()
    if reset_form.validate_on_submit():
        user = User.query.filter_by(email=reset_form.email.data).first()
        if user:
            token = user.reset_password_token()
            send_email(user.email, 'Reset your password',
                       'auth/email/password_reset', user=user, token=token)
            flash('An email containing a reset instructions has been send to your mailtrap address', category='success')
            return redirect(url_for('auth.login'))
    return render_template('auth/reset_password.html', reset_form=reset_form)

# Route that handles reset password token
@auth.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    user = User.confirm_reset_token(token)
    if user is None:
        flash('The confirmation link is invalid or has expired', category='danger')
        return redirect(url_for('main.landing'))
    if not user.is_anonymous:
        return redirect(url_for('main.landing'))
    reset = PasswordResetForm()
    if reset.validate_on_submit():
        user.password=reset.password1.data
        db.session.add(user)
        db.session.commit()
        flash('Your password has been updated',category='success')
        return redirect(url_for('auth.login'))
    else:
        flash('Invalid email or password',category='danger')
    return render_template('auth/reset_password.html',reset=reset)        
      

# login out
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been Signed Out!', category='info')
    return redirect(url_for('auth.login'))
