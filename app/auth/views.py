import email
from flask import render_template
from app.auth import auth
from .forms import RegistrationForm
from app.models import User
from app import db


@auth.route('/register',methods=['GET','POST'])
def register():
    form=RegistrationForm()
    if form.validate_on_submit():
        new_user=User(username=form.username.data,email=form.email.data,password_hash=form.password1.data)
        db.session.add(new_user)
        db.session.commit()
    return render_template('auth/register.html',form=form)
