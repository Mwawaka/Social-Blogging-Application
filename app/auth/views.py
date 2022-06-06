from flask import render_template
from app.auth import auth
from .forms import RegistrationForm

@auth.route('/register',methods=['GET','POST'])
def register():
    form=RegistrationForm()
    return render_template('auth/registration.html',form=form)